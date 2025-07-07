#!/usr/bin/env python3
"""
Debug script to check page 16 of Shorter Catechism
"""

import fitz

def debug_page_16():
    doc = fitz.open('sources/Shorter_Catechism.pdf')
    page = doc.load_page(15)  # Page 16 (0-indexed)
    text = page.get_text()
    print("=== PAGE 16 TEXT ===")
    print(text)
    doc.close()

if __name__ == "__main__":
    debug_page_16() 