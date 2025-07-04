#!/usr/bin/env python3
"""
Debug script to find page markers in the Westminster Shorter Catechism PDF
"""

import fitz  # PyMuPDF
import re

def debug_page_markers(pdf_path: str):
    """Debug what page markers exist in the PDF."""
    doc = fitz.open(pdf_path)
    print(f"PDF has {len(doc)} pages")
    
    # Check each page for bottom markers
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.splitlines()
        
        # Check the last 10 lines for page markers
        for i, line in enumerate(lines[-10:]):
            line = line.strip()
            if re.match(r'^\(\s*\d+\s*\)$', line):
                print(f"Page {page_num+1}: Found marker '{line}' at line {len(lines)-10+i+1}")
        
        # Also check for any lines that contain numbers in parentheses
        for i, line in enumerate(lines):
            if re.search(r'\(\s*\d+\s*\)', line):
                print(f"Page {page_num+1}: Line {i+1}: '{line}'")
    
    doc.close()

if __name__ == "__main__":
    debug_page_markers("sources/Shorter_Catechism.pdf") 