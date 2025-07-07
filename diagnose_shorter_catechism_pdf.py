#!/usr/bin/env python3
"""
Diagnostic script for Westminster Shorter Catechism PDF
Examines the PDF structure to understand footnote parsing requirements
"""

import pdfplumber
import json
from pathlib import Path
from typing import Dict, List, Any

def examine_pdf_structure():
    """Examine the PDF structure to understand footnote format and anomalies."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== WESTMINSTER SHORTER CATECHISM PDF DIAGNOSTIC ===")
    print(f"Examining PDF: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")
        
        # Start examining from page 17 (index 16)
        start_page = 16
        end_page = min(start_page + 10, total_pages)  # Examine 10 pages starting from page 17
        
        print(f"\n=== EXAMINING PAGES {start_page + 1} to {end_page} ===")
        
        for page_num in range(start_page, end_page):
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            
            if not page_text:
                print(f"Page {page_num + 1}: No text extracted")
                continue
                
            print(f"\n--- PAGE {page_num + 1} ---")
            print(f"Text length: {len(page_text)} characters")
            print("First 500 characters:")
            print(page_text[:500])
            print("...")
            
            # Look for footnote patterns
            lines = page_text.split('\n')
            print(f"Number of lines: {len(lines)}")
            
            # Look for superscript numbers (footnote markers)
            superscript_patterns = []
            for i, line in enumerate(lines):
                line = line.strip()
                if line and any(char.isdigit() for char in line[:3]):
                    # Check if it starts with a number (potential footnote)
                    if line[0].isdigit():
                        superscript_patterns.append((i, line[:100]))
            
            if superscript_patterns:
                print(f"Potential footnote patterns found: {len(superscript_patterns)}")
                for line_num, pattern in superscript_patterns[:5]:  # Show first 5
                    print(f"  Line {line_num}: {pattern}")
            else:
                print("No obvious footnote patterns found")
            
            # Look for bold text patterns (scripture references)
            # We'll need to examine the PDF objects for this
            print("\nExamining PDF objects for font information...")
            
            # Extract words with their font information
            words = page.extract_words()
            bold_words = []
            for word in words:
                if 'fontname' in word and 'Bold' in word['fontname']:
                    bold_words.append(word)
            
            if bold_words:
                print(f"Bold text found: {len(bold_words)} words")
                for word in bold_words[:10]:  # Show first 10
                    print(f"  '{word['text']}' (font: {word.get('fontname', 'unknown')})")
            else:
                print("No bold text detected")
            
            # Look for page numbers in parentheses
            import re
            page_number_pattern = r'\(\d+\)'
            page_numbers = re.findall(page_number_pattern, page_text)
            if page_numbers:
                print(f"Page numbers found: {page_numbers}")
            
            print("-" * 50)

def examine_font_information():
    """Examine font information to understand how to identify bold text."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== FONT INFORMATION ANALYSIS ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Examine page 17 (index 16)
        page = pdf.pages[16]
        
        # Extract all text objects with their properties
        chars = page.chars
        print(f"Total characters on page 17: {len(chars)}")
        
        # Group characters by font
        fonts = {}
        for char in chars:
            font_name = char.get('fontname', 'unknown')
            if font_name not in fonts:
                fonts[font_name] = []
            fonts[font_name].append(char)
        
        print(f"Fonts found: {len(fonts)}")
        for font_name, chars_list in fonts.items():
            print(f"  {font_name}: {len(chars_list)} characters")
            # Show first few characters from each font
            sample_text = ''.join([c['text'] for c in chars_list[:20]])
            print(f"    Sample: {sample_text}")
        
        # Look for superscript numbers specifically
        superscript_chars = [c for c in chars if c.get('size', 0) < 10]  # Small font size
        if superscript_chars:
            print(f"\nSuperscript/small characters found: {len(superscript_chars)}")
            sample_superscript = ''.join([c['text'] for c in superscript_chars[:50]])
            print(f"Sample: {sample_superscript}")

def examine_footnote_start():
    """Find where footnotes actually start in the PDF."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== FINDING FOOTNOTE START ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Search through pages to find the first footnote
        for page_num in range(16, min(30, len(pdf.pages))):  # Check pages 17-30
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            
            if not page_text:
                continue
            
            # Look for the pattern "1 Psalm" or "¹ Psalm" (first footnote)
            import re
            patterns = [
                r'^1\s+Psalm',
                r'^¹\s+Psalm',
                r'^\d+\s+Psalm',
                r'^[¹²³⁴⁵⁶⁷⁸⁹]\s+Psalm'
            ]
            
            for pattern in patterns:
                if re.search(pattern, page_text, re.MULTILINE):
                    print(f"Found potential footnote start on page {page_num + 1}")
                    print(f"Pattern matched: {pattern}")
                    print("Page text preview:")
                    print(page_text[:1000])
                    return page_num + 1
        
        print("No clear footnote start found in pages 17-30")

if __name__ == "__main__":
    examine_pdf_structure()
    examine_font_information()
    examine_footnote_start() 