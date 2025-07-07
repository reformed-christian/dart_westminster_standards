#!/usr/bin/env python3
"""
Corrected test script to verify footnote identification with better regex
"""

import pdfplumber
import re
from typing import List, Dict, Set

def test_corrected_footnote_identification():
    """Test to verify we can identify all 227 footnotes correctly with improved regex."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== TESTING CORRECTED FOOTNOTE IDENTIFICATION ===")
    
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
        footnote_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit():
                # Improved pattern: number followed by space OR colon
                if re.match(r'^\d+[\s:]', line):
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
        
        # Show some examples of different footnote formats
        print(f"\nExamples of different footnote formats:")
        format_examples = {}
        for line_num, line in footnote_lines[:20]:
            match = re.match(r'^(\d+)([\s:])(.+)', line)
            if match:
                number, separator, rest = match.groups()
                format_key = f"{number}{separator}"
                if format_key not in format_examples:
                    format_examples[format_key] = line[:80] + "..."
        
        for format_key, example in format_examples.items():
            print(f"  {format_key}: {example}")

def test_footnote_parsing_strategy():
    """Test the strategy for parsing footnotes into references and text."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== TESTING FOOTNOTE PARSING STRATEGY ===")
    
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
        
        # Test parsing strategy on first few footnotes
        current_footnote = None
        current_text = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit() and re.match(r'^\d+[\s:]', line):
                # This is a new footnote
                if current_footnote:
                    print(f"  Footnote {current_footnote}: {len(current_text)} text lines")
                    if current_text:
                        print(f"    Sample text: {current_text[0][:60]}...")
                
                match = re.match(r'^(\d+)', line)
                if match:
                    current_footnote = int(match.group(1))
                    current_text = [line]
                
                if current_footnote and current_footnote > 10:  # Stop after 10 footnotes
                    break
            elif line and current_footnote:
                # This is continuation text for current footnote
                current_text.append(line)
        
        print(f"Parsing strategy test completed for first {current_footnote} footnotes")

if __name__ == "__main__":
    test_corrected_footnote_identification()
    test_footnote_parsing_strategy() 