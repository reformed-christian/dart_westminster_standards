#!/usr/bin/env python3
"""
Test script to verify footnote identification and page number detection
"""

import pdfplumber
import re
from typing import List, Dict, Set

def test_footnote_identification():
    """Test to verify we can identify all 227 footnotes correctly."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== TESTING FOOTNOTE IDENTIFICATION ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Start from page 17 (index 16)
        start_page = 16
        
        # Extract all text from footnote pages
        all_text = ""
        for page_num in range(start_page, len(pdf.pages)):
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
        
        # Find all footnote lines
        lines = all_text.split('\n')
        footnote_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit():
                # Check if it looks like a footnote (number followed by book name)
                if re.match(r'^\d+\s+[A-Z]', line):
                    footnote_lines.append((i, line))
        
        # Extract footnote numbers
        footnote_numbers = []
        for line_num, line in footnote_lines:
            match = re.match(r'^(\d+)', line)
            if match:
                footnote_numbers.append(int(match.group(1)))
        
        # Check for missing footnotes
        expected_footnotes = set(range(1, 228))  # 1 to 227
        found_footnotes = set(footnote_numbers)
        missing_footnotes = expected_footnotes - found_footnotes
        extra_footnotes = found_footnotes - expected_footnotes
        
        print(f"Total footnote lines found: {len(footnote_lines)}")
        print(f"Unique footnote numbers found: {len(found_footnotes)}")
        print(f"Expected footnotes: 1-227")
        print(f"Found footnotes: {sorted(found_footnotes)}")
        
        if missing_footnotes:
            print(f"Missing footnotes: {sorted(missing_footnotes)}")
        else:
            print("✓ All 227 footnotes found!")
        
        if extra_footnotes:
            print(f"Extra footnotes: {sorted(extra_footnotes)}")
        else:
            print("✓ No extra footnotes found!")
        
        # Check for gaps in numbering
        sorted_footnotes = sorted(found_footnotes)
        gaps = []
        for i in range(len(sorted_footnotes) - 1):
            if sorted_footnotes[i+1] - sorted_footnotes[i] > 1:
                gaps.append((sorted_footnotes[i], sorted_footnotes[i+1]))
        
        if gaps:
            print(f"Gaps in numbering: {gaps}")
        else:
            print("✓ No gaps in footnote numbering!")

def test_page_number_detection():
    """Test to verify we can identify all page numbers (1-38)."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== TESTING PAGE NUMBER DETECTION ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Start from page 17 (index 16)
        start_page = 16
        
        page_numbers_found = set()
        
        for page_num in range(start_page, len(pdf.pages)):
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            
            if page_text:
                # Look for page numbers in parentheses
                page_number_matches = re.findall(r'\((\d+)\)', page_text)
                for match in page_number_matches:
                    page_numbers_found.add(int(match))
        
        expected_page_numbers = set(range(1, 39))  # 1 to 38
        missing_page_numbers = expected_page_numbers - page_numbers_found
        extra_page_numbers = page_numbers_found - expected_page_numbers
        
        print(f"Page numbers found: {sorted(page_numbers_found)}")
        print(f"Expected page numbers: 1-38")
        
        if missing_page_numbers:
            print(f"Missing page numbers: {sorted(missing_page_numbers)}")
        else:
            print("✓ All page numbers 1-38 found!")
        
        if extra_page_numbers:
            print(f"Extra page numbers: {sorted(extra_page_numbers)}")
        else:
            print("✓ No extra page numbers found!")

def test_footnote_boundaries():
    """Test to verify we can identify footnote boundaries correctly."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== TESTING FOOTNOTE BOUNDARIES ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Start from page 17 (index 16)
        start_page = 16
        
        # Extract all text from footnote pages
        all_text = ""
        for page_num in range(start_page, len(pdf.pages)):
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
        
        lines = all_text.split('\n')
        
        # Look for blank lines between footnotes
        blank_lines_between_footnotes = 0
        footnote_starts = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check if this is a footnote start
            if line and line[0].isdigit() and re.match(r'^\d+\s+[A-Z]', line):
                footnote_starts += 1
                
                # Check if there's a blank line before this footnote
                if i > 0 and not lines[i-1].strip():
                    blank_lines_between_footnotes += 1
        
        print(f"Total footnote starts found: {footnote_starts}")
        print(f"Blank lines before footnotes: {blank_lines_between_footnotes}")
        print(f"Footnotes without blank lines before: {footnote_starts - blank_lines_between_footnotes}")
        
        # Check first few footnotes to see the pattern
        print("\nFirst 5 footnotes:")
        footnote_count = 0
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit() and re.match(r'^\d+\s+[A-Z]', line):
                footnote_count += 1
                print(f"  Footnote {footnote_count}: {line[:100]}...")
                if footnote_count >= 5:
                    break

def test_superscript_detection():
    """Test to verify we can detect superscript footnote numbers."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== TESTING SUPERSCRIPT DETECTION ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Check first few footnote pages
        for page_num in range(16, 19):  # Pages 17-19
            page = pdf.pages[page_num]
            chars = page.chars
            
            # Look for small, redish characters (potential superscript numbers)
            small_chars = [c for c in chars if c.get('size', 0) < 12]
            redish_chars = [c for c in chars if c.get('stroking_color') == (0.0, 0.0, 0.0) and c.get('non_stroking_color') == (0.0, 0.0, 0.0)]
            
            print(f"Page {page_num + 1}:")
            print(f"  Total characters: {len(chars)}")
            print(f"  Small characters (<12pt): {len(small_chars)}")
            print(f"  Redish characters: {len(redish_chars)}")
            
            # Show first few small characters
            if small_chars:
                small_text = ''.join([c['text'] for c in small_chars[:20]])
                print(f"  Sample small text: {small_text}")

if __name__ == "__main__":
    test_footnote_identification()
    test_page_number_detection()
    test_footnote_boundaries()
    test_superscript_detection() 