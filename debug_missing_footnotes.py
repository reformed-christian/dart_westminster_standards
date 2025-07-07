#!/usr/bin/env python3
"""
Debug script to understand why we're missing 22 footnotes
"""

import pdfplumber
import re
from typing import List, Dict, Set

def debug_missing_footnotes():
    """Debug why we're missing 22 footnotes."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== DEBUGGING MISSING FOOTNOTES ===")
    
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
        
        # Look for all lines that start with numbers
        number_lines = []
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit():
                number_lines.append((i, line))
        
        print(f"Total lines starting with numbers: {len(number_lines)}")
        
        # Check first 20 lines starting with numbers
        print("\nFirst 20 lines starting with numbers:")
        for i, (line_num, line) in enumerate(number_lines[:20]):
            print(f"  {i+1}. Line {line_num}: {line[:100]}...")
        
        # Look for specific missing footnotes
        missing_footnotes = [8, 61, 79, 93, 96, 98, 103, 107, 109, 120, 135, 159, 171, 183, 188, 192, 198, 199, 201, 205, 226, 227]
        
        print(f"\nLooking for missing footnotes: {missing_footnotes}")
        
        for missing in missing_footnotes:
            found = False
            for line_num, line in number_lines:
                if line.startswith(f"{missing} "):
                    print(f"  Found missing footnote {missing}: {line[:100]}...")
                    found = True
                    break
            if not found:
                print(f"  ❌ Missing footnote {missing} not found")
        
        # Check if missing footnotes might be on different lines
        print(f"\nChecking for missing footnotes in different formats:")
        for missing in missing_footnotes:
            found = False
            for line_num, line in number_lines:
                # Check various patterns
                patterns = [
                    f"{missing} ",
                    f"{missing}.",
                    f"{missing}:",
                    f"{missing}\\s",
                ]
                for pattern in patterns:
                    if re.match(pattern, line):
                        print(f"  Found missing footnote {missing} with pattern '{pattern}': {line[:100]}...")
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"  ❌ Missing footnote {missing} not found with any pattern")

def examine_footnote_structure():
    """Examine the structure of footnotes more carefully."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== EXAMINING FOOTNOTE STRUCTURE ===")
    
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
        
        # Look for lines that might be footnotes but don't match our pattern
        potential_footnotes = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit():
                # Check if it doesn't match our current pattern
                if not re.match(r'^\d+\s+[A-Z]', line):
                    potential_footnotes.append((i, line))
        
        print(f"Lines starting with numbers but not matching pattern: {len(potential_footnotes)}")
        
        # Show first 10 potential footnotes
        print("\nFirst 10 potential footnotes:")
        for i, (line_num, line) in enumerate(potential_footnotes[:10]):
            print(f"  {i+1}. Line {line_num}: {line[:100]}...")
        
        # Check if any of these contain missing footnote numbers
        missing_footnotes = [8, 61, 79, 93, 96, 98, 103, 107, 109, 120, 135, 159, 171, 183, 188, 192, 198, 199, 201, 205, 226, 227]
        
        print(f"\nChecking potential footnotes for missing numbers:")
        for missing in missing_footnotes:
            for line_num, line in potential_footnotes:
                if str(missing) in line:
                    print(f"  Found missing footnote {missing} in potential: {line[:100]}...")

def check_page_by_page():
    """Check each page individually for footnotes."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== CHECKING PAGE BY PAGE ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Start from page 17 (index 16)
        start_page = 16
        
        for page_num in range(start_page, len(pdf.pages)):
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            
            if page_text:
                lines = page_text.split('\n')
                footnote_lines = []
                
                for line in lines:
                    line = line.strip()
                    if line and line[0].isdigit():
                        footnote_lines.append(line)
                
                if footnote_lines:
                    print(f"Page {page_num + 1}: {len(footnote_lines)} footnote lines")
                    for line in footnote_lines[:3]:  # Show first 3
                        print(f"  {line[:80]}...")

if __name__ == "__main__":
    debug_missing_footnotes()
    examine_footnote_structure()
    check_page_by_page() 