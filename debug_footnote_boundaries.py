#!/usr/bin/env python3
"""
Debug script to examine footnote extraction boundaries and identify missing footnotes.
"""

import fitz
import re
from collections import defaultdict

def debug_footnote_boundaries(pdf_path: str, start_page: int = 16):
    """Debug how footnotes are being extracted and identify missing ones."""
    
    doc = fitz.open(pdf_path)
    footnote_font = "Times-Roman_7.919999599456787"
    
    # Track all footnote numbers found
    found_numbers = []
    current_footnote = {"number": None, "text": "", "spans": []}
    footnotes = []
    
    print("Scanning for footnote numbers...")
    
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
                            found_numbers.append(int(text.strip().rstrip('.')))
                            
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
    
    print(f"Found {len(found_numbers)} footnote numbers: {sorted(found_numbers)}")
    print(f"Extracted {len(footnotes)} footnotes")
    
    # Check for missing numbers
    if found_numbers:
        min_num = min(found_numbers)
        max_num = max(found_numbers)
        expected_range = set(range(min_num, max_num + 1))
        found_set = set(found_numbers)
        missing = expected_range - found_set
        
        print(f"Footnote numbers range: {min_num} to {max_num}")
        if missing:
            print(f"MISSING footnote numbers: {sorted(missing)}")
        else:
            print("All footnote numbers found!")
    
    # Check for gaps in extracted footnotes
    extracted_numbers = [f["number"] for f in footnotes]
    print(f"Extracted footnote numbers: {sorted(extracted_numbers)}")
    
    if extracted_numbers:
        min_extracted = min(extracted_numbers)
        max_extracted = max(extracted_numbers)
        expected_extracted = set(range(min_extracted, max_extracted + 1))
        extracted_set = set(extracted_numbers)
        missing_extracted = expected_extracted - extracted_set
        
        if missing_extracted:
            print(f"MISSING extracted footnotes: {sorted(missing_extracted)}")
        else:
            print("All footnotes extracted!")
    
    # Look at specific missing footnotes
    if missing:
        print(f"\nExamining missing footnotes around {list(missing)[:5]}...")
        for missing_num in list(missing)[:5]:
            print(f"\nLooking for footnote {missing_num}:")
            # Search for this number in the text
            for page_num in range(start_page, len(doc)):
                page = doc[page_num]
                text_dict = page.get_text("dict")
                
                for block in text_dict.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text = span.get("text", "")
                                if str(missing_num) in text:
                                    font_name = span.get("font", "")
                                    font_size = span.get("size", 0)
                                    font_key = f"{font_name}_{font_size}"
                                    print(f"  Found '{text}' with font: {font_key} on page {page_num + 1}")

if __name__ == "__main__":
    debug_footnote_boundaries("sources/Shorter_Catechism-prts.pdf") 