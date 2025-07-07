#!/usr/bin/env python3
"""
Show which footnote numbers contain unusual numbers
"""

import pdfplumber
import re

def show_unusual_number_footnotes():
    """Show exactly which footnote numbers contain unusual numbers."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== UNUSUAL NUMBERS BY FOOTNOTE ===")
    
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
        
        # Check each footnote for unusual numbers
        unusual_footnotes = []
        
        for line_num, line in footnote_lines:
            # Extract footnote number
            match = re.match(r'^(\d+)', line)
            if not match:
                continue
                
            footnote_num = int(match.group(1))
            
            # Look for numbers followed by capital letters in the footnote text
            # This would be like "1 Corinthians" or "2 Peter" in the scripture text
            number_matches = re.findall(r'\b(\d+)\s+[A-Z]', line)
            
            for num in number_matches:
                if int(num) <= 227:  # Valid footnote range
                    unusual_footnotes.append((footnote_num, num, line[:100]))
        
        # Group by footnote number
        footnote_groups = {}
        for footnote_num, num, text in unusual_footnotes:
            if footnote_num not in footnote_groups:
                footnote_groups[footnote_num] = []
            footnote_groups[footnote_num].append((num, text))
        
        print(f"Found {len(footnote_groups)} footnotes with unusual numbers:")
        
        for footnote_num in sorted(footnote_groups.keys()):
            print(f"\nFootnote {footnote_num}:")
            for num, text in footnote_groups[footnote_num]:
                print(f"  Contains number {num}: {text}...")
        
        # Also show the specific examples from the previous analysis
        print(f"\n=== SPECIFIC EXAMPLES FROM PREVIOUS ANALYSIS ===")
        specific_examples = [
            (17, "1", "all things: to whom be glory for ever. Amen. 1 Corinthians 6:20, 31"),
            (43, "1", "concerning me. 1 Corinthians 2:13"),
            (44, "1", "teacheth, but which the Holy Ghost teacheth; comparing spiritual things with spiritual. 1 Corinthians 14:37"),
            (46, "2", "you are the commandments of the Lord. 2 Peter 1:20-21"),
            (49, "2", "men of God spake as they were moved by the Holy Ghost. 2 Peter 3:2, 15-16"),
            (68, "2", "scriptures daily, whether those things were so. 2 Timothy 3:15-17"),
            (139, "1", "now their God? But our God is in the heavens: he hath done whatsoever he hath pleased. 1 Timothy 1:17"),
            (141, "1", "Amen. 1 Timothy 6:15-16"),
            (149, "1", "but all things are naked and opened unto the eyes of him with whom we have to do. 1 John 3:20"),
            (159, "1", "enemies thy footstool? 1 Peter 1:15-16"),
            (160, "1", "of conversation; Because it is written, Be ye holy; for I am holy. 1 John 3:3, 5")
        ]
        
        print("These line numbers correspond to text within footnotes:")
        for line_num, num, text in specific_examples:
            print(f"Line {line_num}: Number {num} in '{text}...'")

if __name__ == "__main__":
    show_unusual_number_footnotes() 