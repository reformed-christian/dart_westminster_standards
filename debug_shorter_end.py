#!/usr/bin/env python3
"""
Debug script to find the end of Shorter Catechism questions
"""

import fitz

def debug_shorter_end():
    doc = fitz.open('sources/Shorter_Catechism.pdf')
    
    # Check the last few pages
    for page_num in range(len(doc) - 5, len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        print(f"\n=== PAGE {page_num + 1} ===")
        print(text[:500])  # First 500 chars
        print("...")
        print(text[-500:])  # Last 500 chars
    
    doc.close()

if __name__ == "__main__":
    debug_shorter_end() 