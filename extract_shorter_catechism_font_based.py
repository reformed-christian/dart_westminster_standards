#!/usr/bin/env python3
"""
Extract Westminster Shorter Catechism footnote references using font detection.
This script finds footnotes by detecting the unique font used for footnote numbers,
then extracts all bold scripture references from each footnote.
"""

import fitz
import json
import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

def extract_footnotes_by_font(pdf_path: str, start_page: int = 16) -> List[Dict]:
    """
    Extract footnotes by finding text with the footnote font.
    Each footnote starts with a number in a specific font.
    """
    doc = fitz.open(pdf_path)
    footnotes = []
    
    # First, let's analyze the fonts to find the footnote font
    footnote_font = None
    font_samples = defaultdict(int)
    
    print("Analyzing fonts to find footnote font...")
    
    for page_num in range(start_page, len(doc)):
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_name = span.get("font", "")
                        font_size = span.get("size", 0)
                        text = span.get("text", "").strip()
                        
                        # Look for patterns that indicate footnote numbers
                        if re.match(r'^\d+\.?$', text):
                            font_key = f"{font_name}_{font_size}"
                            font_samples[font_key] += 1
                            print(f"Potential footnote number '{text}' with font: {font_key}")
    
    # Find the most common font for footnote numbers
    if font_samples:
        footnote_font = max(font_samples.items(), key=lambda x: x[1])[0]
        print(f"Selected footnote font: {footnote_font} (used {font_samples[footnote_font]} times)")
    else:
        print("No footnote fonts found!")
        return []
    
    # Now extract footnotes using the identified font
    current_footnote = {"number": None, "text": "", "page": None}
    
    for page_num in range(start_page, len(doc)):
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_name = span.get("font", "")
                        font_size = span.get("size", 0)
                        font_key = f"{font_name}_{font_size}"
                        text = span.get("text", "")
                        flags = span.get("flags", 0)
                        is_bold = flags & 2**4  # Bold flag
                        
                        # Check if this is a footnote number
                        if font_key == footnote_font and re.match(r'^\d+\.?$', text.strip()):
                            # Save previous footnote if it exists
                            if current_footnote["number"] is not None:
                                footnotes.append(current_footnote.copy())
                            
                            # Start new footnote
                            current_footnote = {
                                "number": int(text.strip().rstrip('.')),
                                "text": text,
                                "page": page_num + 1,
                                "spans": []
                            }
                        elif current_footnote["number"] is not None:
                            # Add to current footnote
                            current_footnote["text"] += text
                            current_footnote["spans"].append({
                                "text": text,
                                "font": font_name,
                                "size": font_size,
                                "flags": flags,
                                "is_bold": is_bold
                            })
    
    # Add the last footnote
    if current_footnote["number"] is not None:
        footnotes.append(current_footnote)
    
    print(f"Extracted {len(footnotes)} footnotes using font detection")
    
    # Sort by footnote number
    footnotes.sort(key=lambda x: x["number"])
    
    # Print first few footnotes for debugging
    for i, footnote in enumerate(footnotes[:5]):
        print(f"Footnote {footnote['number']}: {footnote['text'][:100]}...")
    
    return footnotes

def extract_references_from_footnotes(footnotes: List[Dict]) -> List[Dict]:
    """
    Extract scripture references from each footnote.
    Look for bold text that matches scripture reference patterns.
    """
    references = []
    
    for footnote in footnotes:
        footnote_num = footnote["number"]
        spans = footnote.get("spans", [])
        
        # Extract all bold spans
        bold_spans = [span for span in spans if span.get("is_bold", False)]
        
        # Process each bold span as a potential reference
        for span in bold_spans:
            text = span["text"].strip()
            if not text:
                continue
            
            # Clean the reference - remove leading numbers and periods
            cleaned_ref = re.sub(r'^[\d\s\.]+', '', text).strip()
            cleaned_ref = re.sub(r'\.$', '', cleaned_ref)
            
            # More permissive reference detection - any bold text that looks like a reference
            if (cleaned_ref and 
                len(cleaned_ref) > 2 and  # At least 3 characters
                re.match(r'^[A-Za-z\s\d:,]+$', cleaned_ref) and  # Only letters, spaces, numbers, colons, commas
                (re.search(r'\d+:\d+', cleaned_ref) or  # Contains chapter:verse
                 re.match(r'^[A-Z][a-z]+', cleaned_ref) or  # Starts with capital letter (book name)
                 re.match(r'^\d+\s+[A-Z][a-z]+', cleaned_ref) or  # Number followed by book name
                 re.match(r'^[A-Z][a-z]+\s+\d+', cleaned_ref))):  # Book name followed by number
                
                # Extract the scripture text (everything after this reference until the next reference)
                ref_start = footnote["text"].find(text)
                if ref_start != -1:
                    ref_end = ref_start + len(text)
                    scripture_text = footnote["text"][ref_end:].strip()
                    
                    # Find the next bold reference to cut off the scripture text
                    next_ref_start = -1
                    for next_span in bold_spans:
                        if next_span != span:
                            next_text = next_span["text"].strip()
                            next_pos = footnote["text"].find(next_text, ref_end)
                            if next_pos != -1 and (next_ref_start == -1 or next_pos < next_ref_start):
                                next_ref_start = next_pos
                    
                    if next_ref_start != -1:
                        scripture_text = footnote["text"][ref_end:next_ref_start].strip()
                    
                    # Clean scripture text
                    scripture_text = re.sub(r'\s+', ' ', scripture_text)
                    scripture_text = re.sub(r'^\d+\s*', '', scripture_text)  # Remove page numbers
                    
                    references.append({
                        "footnote_number": footnote_num,
                        "reference": cleaned_ref,
                        "scripture_text": scripture_text,
                        "page": footnote["page"]
                    })
    
    return references

def main():
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("Extracting footnotes using font detection...")
    footnotes = extract_footnotes_by_font(pdf_path)
    
    if not footnotes:
        print("No footnotes found!")
        return
    
    print(f"\nFound {len(footnotes)} footnotes")
    
    # Check for gaps in numbering
    numbers = [f["number"] for f in footnotes]
    print(f"Footnote numbers range: {min(numbers)} to {max(numbers)}")
    
    missing = []
    for i in range(min(numbers), max(numbers) + 1):
        if i not in numbers:
            missing.append(i)
    
    if missing:
        print(f"Missing footnote numbers: {missing}")
    
    print("\nExtracting references from footnotes...")
    references = extract_references_from_footnotes(footnotes)
    
    print(f"Extracted {len(references)} references")
    
    # Convert to the expected format (dictionary)
    output_references = {}
    for ref in references:
        key = str(ref["footnote_number"])
        entry = {
            "reference": ref["reference"],
            "text": ref["scripture_text"]
        }
        if key not in output_references:
            output_references[key] = []
        output_references[key].append(entry)

    # Save to JSON
    output_file = "westminster_shorter_catechism_references_font_based_dict.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_references, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {sum(len(v) for v in output_references.values())} references to {output_file}")
    print(f"\nFirst 3 footnotes:")
    for k in sorted(output_references.keys(), key=lambda x: int(x))[:3]:
        print(f"  Footnote {k}: {output_references[k]}")

if __name__ == "__main__":
    main() 