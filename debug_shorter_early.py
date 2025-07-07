#!/usr/bin/env python3
"""
Debug script to check early pages of Shorter Catechism
"""

import fitz
import re

def debug_shorter_early():
    doc = fitz.open('sources/Shorter_Catechism.pdf')
    
    # Check early pages
    for page_num in range(0, 15):
        page = doc.load_page(page_num)
        text = page.get_text()
        print(f"\n=== PAGE {page_num + 1} ===")
        
        # Look for question patterns
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'Q\.\s*\d+\.', line):
                print(f"Line {i}: {line.strip()}")
            elif re.search(r'A\.\s*', line):
                print(f"Line {i}: {line.strip()}")
    
    doc.close()

if __name__ == "__main__":
    debug_shorter_early() 