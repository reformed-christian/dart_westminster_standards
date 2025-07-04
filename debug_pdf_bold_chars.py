#!/usr/bin/env python3
"""
Debug PDF Bold Text Detection using pdfplumber extract_chars
"""

import pdfplumber
import re
from pathlib import Path

def debug_bold_chars(pdf_path: str):
    print(f"🔍 Checking for bold text/font info in: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF has {len(pdf.pages)} pages")
        # Find the page with (15) marker
        start_page = None
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = text.splitlines()
            for line in lines[-5:]:
                if re.match(r"^\(\s*15\s*\)$", line.strip()):
                    start_page = i
                    print(f"✅ Found page (15) at PDF page {i+1}")
                    break
            if start_page is not None:
                break
        if start_page is None:
            print("❌ Could not find page with (15) marker")
            return
        page = pdf.pages[start_page]
        print(f"\nExamining PDF page {start_page+1} for character font info:")
        # Try extract_chars
        if hasattr(page, 'extract_chars'):
            chars = page.extract_chars()
            print(f"Found {len(chars)} character objects. Showing first 100:")
            for i, char in enumerate(chars[:100]):
                font = char.get('fontname', 'unknown')
                size = char.get('size', 0)
                text = char.get('text', '')
                print(f"  Char {i+1}: '{text}' | Font: {font} | Size: {size}")
        else:
            print("❌ This version of pdfplumber does not support extract_chars().")

def main():
    pdf_path = "sources/Shorter_Catechism.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return
    debug_bold_chars(pdf_path)

if __name__ == "__main__":
    main() 