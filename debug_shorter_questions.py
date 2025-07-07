#!/usr/bin/env python3
"""
Debug script to find where Shorter Catechism questions end
"""

import fitz
import re

def debug_shorter_questions():
    doc = fitz.open('sources/Shorter_Catechism.pdf')
    
    # Check pages around where we expect questions to end
    for page_num in range(20, 35):
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
    debug_shorter_questions() 