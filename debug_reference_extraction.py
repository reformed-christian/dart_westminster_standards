#!/usr/bin/env python3
"""
Debug script to examine why some footnotes are missing references.
"""

import fitz
import json
import re
from collections import defaultdict

def debug_reference_extraction(pdf_path: str, start_page: int = 16):
    """Debug why some footnotes are missing references."""
    
    doc = fitz.open(pdf_path)
    footnote_font = "Times-Roman_7.919999599456787"
    
    # Extract footnotes first
    current_footnote = {"number": None, "text": "", "spans": []}
    footnotes = []
    
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
    
    # Sort by footnote number
    footnotes.sort(key=lambda x: x["number"])
    
    # Analyze reference extraction for each footnote
    footnotes_with_refs = 0
    footnotes_without_refs = []
    
    for footnote in footnotes:
        footnote_num = footnote["number"]
        spans = footnote.get("spans", [])
        
        # Extract all bold spans
        bold_spans = [span for span in spans if span.get("is_bold", False)]
        
        # Count potential references
        potential_refs = []
        for span in bold_spans:
            text = span["text"].strip()
            if text and re.match(r'^[A-Za-z\s\d:,\.]+$', text):
                if (re.search(r'\d+:\d+', text) or  # Contains chapter:verse
                    re.match(r'^[A-Z][a-z]+', text) or  # Starts with capital letter (book name)
                    re.match(r'^\d+\s+[A-Z][a-z]+', text)):  # Number followed by book name
                    potential_refs.append(text)
        
        if potential_refs:
            footnotes_with_refs += 1
        else:
            footnotes_without_refs.append(footnote_num)
    
    print(f"Total footnotes: {len(footnotes)}")
    print(f"Footnotes with references: {footnotes_with_refs}")
    print(f"Footnotes without references: {len(footnotes_without_refs)}")
    
    if footnotes_without_refs:
        print(f"Footnotes missing references: {footnotes_without_refs[:20]}...")
        
        # Examine a few footnotes that should have references but don't
        for missing_num in footnotes_without_refs[:5]:
            footnote = next(f for f in footnotes if f["number"] == missing_num)
            print(f"\n=== Footnote {missing_num} (Page {footnote['page']}) ===")
            print(f"Full text: {footnote['text'][:200]}...")
            
            # Show all bold spans
            bold_spans = [span for span in footnote["spans"] if span.get("is_bold", False)]
            print(f"Bold spans ({len(bold_spans)}):")
            for i, span in enumerate(bold_spans):
                text = span["text"].strip()
                if text:
                    print(f"  {i}: '{text}' | Font: {span['font']}_{span['size']}")
            
            # Show all spans that might be references
            print(f"All spans that might be references:")
            for i, span in enumerate(footnote["spans"]):
                text = span["text"].strip()
                if text and re.match(r'^[A-Za-z\s\d:,\.]+$', text):
                    if (re.search(r'\d+:\d+', text) or 
                        re.match(r'^[A-Z][a-z]+', text) or 
                        re.match(r'^\d+\s+[A-Z][a-z]+', text)):
                        print(f"  {i}: '{text}' | Font: {span['font']}_{span['size']} | Bold: {span.get('is_bold', False)}")

if __name__ == "__main__":
    debug_reference_extraction("sources/Shorter_Catechism-prts.pdf") 