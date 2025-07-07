#!/usr/bin/env python3
"""
Debug script to examine footnote content and understand why only 32 references are found.
"""

import fitz
import re
from collections import defaultdict

def debug_footnote_content(pdf_path: str, start_page: int = 16, num_footnotes: int = 10):
    """Debug the content of the first few footnotes to understand the structure."""
    
    doc = fitz.open(pdf_path)
    
    # Find the footnote font
    footnote_font = "Times-Roman_7.919999599456787"
    
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
        
        # Stop after collecting enough footnotes
        if len(footnotes) >= num_footnotes:
            break
    
    # Add the last footnote
    if current_footnote["number"] is not None and len(footnotes) < num_footnotes:
        footnotes.append(current_footnote)
    
    # Debug each footnote
    for i, footnote in enumerate(footnotes):
        print(f"\n{'='*60}")
        print(f"FOOTNOTE {footnote['number']} (Page {footnote['page']})")
        print(f"{'='*60}")
        print(f"Full text: {footnote['text']}")
        print(f"\nSpans breakdown:")
        
        for j, span in enumerate(footnote['spans']):
            text = span['text'].strip()
            if text:  # Only show non-empty spans
                font_info = f"{span['font']}_{span['size']}"
                bold_marker = " [BOLD]" if span['is_bold'] else ""
                print(f"  {j:2d}: '{text}' | Font: {font_info}{bold_marker}")
        
        # Look for potential scripture references (any text that looks like a reference)
        potential_refs = []
        for span in footnote['spans']:
            text = span['text'].strip()
            if re.match(r'^[A-Za-z\s\d:,\.]+$', text) and len(text) > 2:
                # Check if it looks like a scripture reference
                if re.search(r'\d+:\d+', text) or re.match(r'^[A-Z][a-z]+', text):
                    potential_refs.append({
                        'text': text,
                        'font': f"{span['font']}_{span['size']}",
                        'is_bold': span['is_bold']
                    })
        
        if potential_refs:
            print(f"\nPotential scripture references:")
            for ref in potential_refs:
                bold_marker = " [BOLD]" if ref['is_bold'] else ""
                print(f"  '{ref['text']}' | Font: {ref['font']}{bold_marker}")
        else:
            print(f"\nNo potential scripture references found")

if __name__ == "__main__":
    debug_footnote_content("sources/Shorter_Catechism-prts.pdf") 