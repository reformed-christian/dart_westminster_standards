#!/usr/bin/env python3
"""
Final extraction script for Westminster Shorter Catechism footnote references.
This version properly handles split references and combines them correctly.
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
    
    # Find the footnote font
    footnote_font = "Times-Roman_7.919999599456787"
    
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
                        is_bold = flags & 2**4
                        
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
    
    return footnotes

def extract_references_from_footnotes(footnotes: List[Dict]) -> List[Dict]:
    """
    Extract scripture references from each footnote.
    Properly handle split references by combining consecutive bold spans.
    """
    references = []
    
    # Common book name mappings for missing numbers
    book_mappings = {
        "Corinthians": "1 Corinthians",
        "Kings": "1 Kings", 
        "Timothy": "2 Timothy",
        "Peter": "1 Peter",
        "Thessalonians": "1 Thessalonians",
        "John": "1 John"
    }
    
    for footnote in footnotes:
        footnote_num = footnote["number"]
        spans = footnote.get("spans", [])
        
        # Extract all bold spans
        bold_spans = [span for span in spans if span.get("is_bold", False)]
        
        # Combine consecutive bold spans that belong to the same reference
        combined_refs = []
        current_ref_parts = []
        
        for i, span in enumerate(bold_spans):
            text = span["text"].strip()
            if not text:
                continue
            
            # Check if this span should be combined with the previous one
            should_combine = False
            
            if current_ref_parts:
                # If previous part ends with a number and this starts with a colon, combine
                prev_text = current_ref_parts[-1]["text"]
                if (re.search(r'\d$', prev_text) and text.startswith(':')) or \
                   (re.search(r'\d$', prev_text) and text.startswith(',')) or \
                   (re.search(r'\d$', prev_text) and text.startswith('-')) or \
                   (re.search(r'\d$', prev_text) and text.startswith('.')):
                    should_combine = True
                # If this is just a number and previous part is a book name, combine
                elif re.match(r'^\d+$', text) and re.match(r'^[A-Z][a-z]+$', prev_text):
                    should_combine = True
                # If this starts with a number and previous part is a book name, combine
                elif re.match(r'^\d+:', text) and re.match(r'^[A-Z][a-z]+$', prev_text):
                    should_combine = True
                # If this is a verse range and previous part ends with a number, combine
                elif re.match(r'^\d+-\d+', text) and re.search(r'\d$', prev_text):
                    should_combine = True
            
            if should_combine:
                current_ref_parts.append(span)
            else:
                # Save the current reference if we have one
                if current_ref_parts:
                    combined_refs.append(current_ref_parts)
                # Start a new reference
                current_ref_parts = [span]
        
        # Add the last reference
        if current_ref_parts:
            combined_refs.append(current_ref_parts)
        
        # Process each combined reference
        for ref_parts in combined_refs:
            # Combine all parts into one reference
            full_ref = ''.join(part["text"] for part in ref_parts)
            
            # Clean the reference
            cleaned_ref = re.sub(r'^[\d\s\.]+', '', full_ref).strip()
            cleaned_ref = re.sub(r'\.$', '', cleaned_ref)
            
            # Additional cleaning for common issues
            cleaned_ref = re.sub(r'^With\s+', '', cleaned_ref)  # Remove "With" prefix
            
            # Fix missing book numbers
            for short_name, full_name in book_mappings.items():
                if cleaned_ref.startswith(short_name + " "):
                    cleaned_ref = cleaned_ref.replace(short_name, full_name, 1)
                    break
            
            # Check if this looks like a valid scripture reference
            if (cleaned_ref and 
                len(cleaned_ref) > 2 and
                re.match(r'^[A-Za-z\s\d:,]+$', cleaned_ref) and
                (re.search(r'\d+:\d+', cleaned_ref) or  # Contains chapter:verse
                 re.match(r'^[A-Z][a-z]+', cleaned_ref) or  # Starts with capital letter (book name)
                 re.match(r'^\d+\s+[A-Z][a-z]+', cleaned_ref) or  # Number followed by book name
                 re.match(r'^[A-Z][a-z]+\s+\d+', cleaned_ref))):  # Book name followed by number
                
                # Extract the scripture text
                ref_start = footnote["text"].find(full_ref)
                if ref_start != -1:
                    ref_end = ref_start + len(full_ref)
                    scripture_text = footnote["text"][ref_end:].strip()
                    
                    # Find the next reference to cut off the scripture text
                    next_ref_start = -1
                    for other_ref_parts in combined_refs:
                        if other_ref_parts != ref_parts:
                            other_full_ref = ''.join(part["text"] for part in other_ref_parts)
                            next_pos = footnote["text"].find(other_full_ref, ref_end)
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
    output_file = "westminster_shorter_catechism_references_final.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_references, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {sum(len(v) for v in output_references.values())} references to {output_file}")
    print(f"Footnotes with references: {len(output_references)}")
    
    # Print first few footnotes for verification
    print(f"\nFirst 3 footnotes:")
    for k in sorted(output_references.keys(), key=lambda x: int(x))[:3]:
        print(f"  Footnote {k}: {len(output_references[k])} references")

if __name__ == "__main__":
    main() 