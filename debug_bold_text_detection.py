#!/usr/bin/env python3
"""
Debug script to see what bold text is actually being detected
"""

import fitz  # PyMuPDF
import re

def debug_bold_text():
    """Debug what bold text is being detected in the PDF."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== DEBUGGING BOLD TEXT DETECTION ===")
    
    with fitz.open(pdf_path) as doc:
        # Start from page 17 (index 16)
        start_page = 16
        
        # Check first few pages
        for page_num in range(start_page, start_page + 3):  # Pages 17-19
            page = doc[page_num]
            
            print(f"\n--- Page {page_num + 1} ---")
            
            # Get text blocks with font information
            blocks = page.get_text("dict")["blocks"]
            
            bold_texts = []
            regular_texts = []
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                if span["flags"] & 16:  # Bold flag
                                    bold_texts.append({
                                        "text": text,
                                        "font": span["font"],
                                        "size": span["size"],
                                        "flags": span["flags"]
                                    })
                                else:
                                    regular_texts.append({
                                        "text": text,
                                        "font": span["font"],
                                        "size": span["size"],
                                        "flags": span["flags"]
                                    })
            
            print(f"Bold texts found: {len(bold_texts)}")
            print("Sample bold texts:")
            for i, item in enumerate(bold_texts[:10]):
                print(f"  {i+1}. '{item['text']}' (font: {item['font']}, size: {item['size']}, flags: {item['flags']})")
            
            print(f"\nRegular texts found: {len(regular_texts)}")
            print("Sample regular texts:")
            for i, item in enumerate(regular_texts[:10]):
                print(f"  {i+1}. '{item['text']}' (font: {item['font']}, size: {item['size']}, flags: {item['flags']})")

def check_footnote_1():
    """Specifically check footnote 1 to see what's happening."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== CHECKING FOOTNOTE 1 SPECIFICALLY ===")
    
    with fitz.open(pdf_path) as doc:
        # Get page 17 (index 16)
        page = doc[16]
        
        # Get the plain text
        page_text = page.get_text()
        lines = page_text.split('\n')
        
        print("First few lines of page 17:")
        for i, line in enumerate(lines[:10]):
            print(f"  {i+1}. {line}")
        
        # Look for footnote 1
        footnote_1_text = ""
        for line in lines:
            if line.strip().startswith('1 '):
                footnote_1_text = line
                break
        
        print(f"\nFootnote 1 text: {footnote_1_text}")
        
        # Now look for bold text in this area
        blocks = page.get_text("dict")["blocks"]
        
        print("\nAll text spans on page 17:")
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text and len(text) > 2:  # Only show meaningful text
                            bold_flag = "BOLD" if span["flags"] & 16 else "regular"
                            print(f"  '{text}' ({bold_flag}, font: {span['font']}, size: {span['size']})")

if __name__ == "__main__":
    debug_bold_text()
    check_footnote_1() 