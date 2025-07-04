#!/usr/bin/env python3
"""
Debug PDF Extraction - Test what formatting information is preserved
"""

import pdfplumber
import re
from pathlib import Path

def debug_pdf_extraction(pdf_path: str):
    """Debug what's being extracted from the PDF"""
    
    print(f"🔍 Debugging PDF extraction from: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"📄 PDF has {len(pdf.pages)} pages")
        
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
        
        # Examine the first few pages from the start page
        for page_num in range(start_page, min(start_page + 3, len(pdf.pages))):
            page = pdf.pages[page_num]
            print(f"\n📖 Examining PDF page {page_num + 1}:")
            
            # Method 1: extract_text()
            print("  Method 1: extract_text()")
            text = page.extract_text() or ""
            lines = text.splitlines()
            print(f"    Found {len(lines)} lines")
            for i, line in enumerate(lines[:10]):
                print(f"    Line {i+1}: {repr(line)}")
            
            # Method 2: extract_words() with formatting
            print("\n  Method 2: extract_words() with formatting")
            words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
            print(f"    Found {len(words)} word objects")
            
            # Look for words with font information
            bold_words = []
            for word in words[:20]:  # First 20 words
                font_info = word.get('fontname', 'unknown')
                size = word.get('size', 0)
                text = word.get('text', '')
                print(f"    Word: {repr(text)} | Font: {font_info} | Size: {size}")
                if 'bold' in font_info.lower() or size > 12:  # Heuristic for bold
                    bold_words.append(word)
            
            print(f"    Potential bold words: {len(bold_words)}")
            for word in bold_words[:5]:
                print(f"      Bold: {repr(word.get('text', ''))}")
            
            # Method 3: Look for footnote patterns in the text
            print("\n  Method 3: Looking for footnote patterns")
            text = page.extract_text() or ""
            # Look for patterns like "80 Psalm", "81 Psalm", etc.
            footnote_pattern = r'^\s*(\d+)\s+([A-Z][a-z]+)'
            matches = re.findall(footnote_pattern, text, re.MULTILINE)
            print(f"    Found {len(matches)} potential footnote patterns:")
            for num, book in matches[:10]:
                print(f"      {num} {book}")
            
            # Method 4: Show the actual content structure
            print("\n  Method 4: Content structure analysis")
            lines = text.splitlines()
            footnote_lines = []
            for i, line in enumerate(lines):
                if re.match(r'^\s*\d+\s+[A-Z]', line):
                    footnote_lines.append((i+1, line[:100]))  # First 100 chars
            
            print(f"    Found {len(footnote_lines)} lines starting with numbers:")
            for line_num, content in footnote_lines[:5]:
                print(f"      Line {line_num}: {repr(content)}")
            
            print("\n" + "="*60)

def main():
    pdf_path = "sources/Shorter_Catechism.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    debug_pdf_extraction(pdf_path)

if __name__ == "__main__":
    main() 