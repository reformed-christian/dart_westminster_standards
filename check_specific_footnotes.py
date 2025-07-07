#!/usr/bin/env python3
"""
Check specific footnotes to see actual bold text content
"""

import pdfplumber
import re

def check_specific_footnotes():
    """Check the actual bold text content for specific footnotes."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== CHECKING SPECIFIC FOOTNOTES ===")
    
    # Footnotes to check: 1, 3, 9, 21, 177, 190, 194, 222
    target_footnotes = [1, 3, 9, 21, 177, 190, 194, 222]
    
    with pdfplumber.open(pdf_path) as pdf:
        # Extract all text from footnote pages
        all_text = ""
        for page_num in range(16, len(pdf.pages)):  # Pages 17 onwards
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
        
        # Find the specific footnotes
        for line_num, line in footnote_lines:
            # Extract footnote number
            match = re.match(r'^(\d+)', line)
            if not match:
                continue
                
            footnote_num = int(match.group(1))
            
            if footnote_num in target_footnotes:
                print(f"\n--- FOOTNOTE {footnote_num} ---")
                print(f"Full line: {line}")
                
                # Now let's get the bold text for this footnote
                # We need to find which page this footnote is on
                for page_num in range(16, len(pdf.pages)):
                    page = pdf.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text and f"{footnote_num} " in page_text:
                        print(f"Found on page {page_num + 1}")
                        
                        # Extract bold characters from this page
                        chars = page.chars
                        bold_chars = [c for c in chars if 'Bold' in c.get('fontname', '')]
                        
                        if bold_chars:
                            bold_text = ''.join([c['text'] for c in bold_chars])
                            print(f"All bold text on page: {bold_text}")
                            
                            # Try to find the specific references for this footnote
                            # Look for patterns that might match this footnote
                            if footnote_num == 1:
                                # Look for Psalm 86, Isaiah 60:21, etc.
                                psalm_match = re.search(r'Psalm\s*86', bold_text)
                                isaiah_match = re.search(r'Isaiah\s*60:\s*21', bold_text)
                                if psalm_match:
                                    print(f"  Found: {psalm_match.group()}")
                                if isaiah_match:
                                    print(f"  Found: {isaiah_match.group()}")
                            
                            elif footnote_num == 3:
                                # Look for "With Genesis"
                                with_match = re.search(r'With\s+Genesis', bold_text)
                                if with_match:
                                    print(f"  Found: {with_match.group()}")
                            
                            elif footnote_num == 9:
                                # Look for "Revelation1:4"
                                rev_match = re.search(r'Revelation\s*1:\s*4', bold_text)
                                if rev_match:
                                    print(f"  Found: {rev_match.group()}")
                            
                            elif footnote_num == 21:
                                # Look for "John"
                                john_match = re.search(r'\bJohn\b', bold_text)
                                if john_match:
                                    print(f"  Found: {john_match.group()}")
                            
                            elif footnote_num == 190:
                                # Look for "1 Corinthians"
                                cor_match = re.search(r'1\s+Corinthians', bold_text)
                                if cor_match:
                                    print(f"  Found: {cor_match.group()}")
                            
                            break

def show_unusual_numbers():
    """Show exactly what the 'unusual numbers' look like."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== SHOWING UNUSUAL NUMBERS ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from first few footnote pages
        all_text = ""
        for page_num in range(16, 20):  # Pages 17-20
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
        
        lines = all_text.split('\n')
        
        print("Lines containing numbers that might be confused with footnotes:")
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line[0].isdigit():  # Not a footnote line
                # Look for numbers followed by capital letters
                number_matches = re.findall(r'\b(\d+)\s+[A-Z]', line)
                for num in number_matches:
                    if int(num) <= 227:  # Valid footnote range
                        print(f"Line {i}: {line[:150]}...")
                        print(f"  Number {num} found in: {line}")
                        break

if __name__ == "__main__":
    check_specific_footnotes()
    show_unusual_numbers() 