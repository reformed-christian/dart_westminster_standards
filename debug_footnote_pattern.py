#!/usr/bin/env python3

import fitz
import re

def debug_footnote_pattern():
    doc = fitz.open('sources/Shorter_Catechism-prts.pdf')
    
    # Extract text from pages 17-20 to see the structure
    plain_text = ""
    for page_num in range(16, 20):  # Pages 17-20 (0-indexed)
        page = doc[page_num]
        page_text = page.get_text()
        plain_text += f"\n--- PAGE {page_num + 1} ---\n"
        plain_text += page_text
    
    print("First 2000 characters of extracted text:")
    print(plain_text[:2000])
    
    print("\n" + "="*80)
    print("Looking for footnote patterns:")
    
    # Try different patterns
    patterns = [
        r'\n(\d+)[\s:]\n',
        r'\n(\d+)[\s:]\s',
        r'(\d+)[\s:]\s',
        r'\n(\d+)\.\s',
        r'(\d+)\.\s'
    ]
    
    for i, pattern in enumerate(patterns):
        matches = list(re.finditer(pattern, plain_text))
        print(f"Pattern {i+1}: {pattern}")
        print(f"  Found {len(matches)} matches")
        if matches:
            print(f"  First 5 matches: {[m.group(0) for m in matches[:5]]}")
        print()
    
    # Look for specific patterns in the text
    print("Searching for specific patterns:")
    lines = plain_text.split('\n')
    for i, line in enumerate(lines[:50]):
        if re.search(r'^\d+', line.strip()):
            print(f"Line {i}: '{line.strip()}'")
    
    doc.close()

if __name__ == "__main__":
    debug_footnote_pattern() 