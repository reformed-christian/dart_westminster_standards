#!/usr/bin/env python3
"""
Identify specific footnotes containing anomalies
"""

import pdfplumber
import re
from typing import Dict, List, Tuple

def identify_footnote_anomalies():
    """Identify exactly which footnotes contain specific anomalies."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== IDENTIFYING FOOTNOTE ANOMALIES ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Start from page 17 (index 16)
        start_page = 16
        
        # Track anomalies by footnote number
        anomalies = {
            'missing_spaces': [],  # e.g., "Isaiah60:21"
            'with_prefix': [],     # e.g., "With Genesis 2:24"
            'incomplete_refs': [], # e.g., "Corinthians" instead of "1 Corinthians"
            'unusual_numbers': []  # numbers in middle of text that aren't footnotes
        }
        
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
        
        print(f"Found {len(footnote_lines)} footnote lines")
        
        # Analyze each footnote
        for line_num, line in footnote_lines:
            # Extract footnote number
            match = re.match(r'^(\d+)', line)
            if not match:
                continue
                
            footnote_num = int(match.group(1))
            
            # Check for missing spaces in references
            # Look for patterns like "BookName1:2" (no space between book and chapter)
            missing_space_pattern = r'([A-Z][a-z]+)(\d+:\d+)'
            missing_space_matches = re.findall(missing_space_pattern, line)
            if missing_space_matches:
                for book, verses in missing_space_matches:
                    ref = f"{book}{verses}"
                    anomalies['missing_spaces'].append((footnote_num, ref))
            
            # Check for "With" prefix
            if "With " in line:
                # Find the reference after "With"
                with_match = re.search(r'With\s+([A-Z][a-zA-Z\s]+(?:\d+)?\s*:\s*\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)', line)
                if with_match:
                    ref = with_match.group(1)
                    anomalies['with_prefix'].append((footnote_num, f"With {ref}"))
            
            # Check for incomplete references
            # Look for standalone "Corinthians", "Timothy", etc. without numbers
            incomplete_patterns = [
                r'\bCorinthians\b(?!\s+\d+)',  # Corinthians not followed by number
                r'\bTimothy\b(?!\s+\d+)',      # Timothy not followed by number
                r'\bPeter\b(?!\s+\d+)',        # Peter not followed by number
                r'\bJohn\b(?!\s+\d+)',         # John not followed by number
            ]
            
            for pattern in incomplete_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    anomalies['incomplete_refs'].append((footnote_num, match))
        
        # Check for unusual numbers in middle of text
        for line_num, line in enumerate(lines):
            line = line.strip()
            if line and not line[0].isdigit():  # Not a footnote line
                # Look for numbers that might be confused with footnotes
                number_matches = re.findall(r'\b(\d+)\s+[A-Z]', line)
                for num in number_matches:
                    if int(num) <= 227:  # Valid footnote range
                        anomalies['unusual_numbers'].append((line_num, num, line[:100]))
        
        # Report findings
        print("\n=== ANOMALY REPORT ===")
        
        print(f"\n1. Missing spaces in references ({len(anomalies['missing_spaces'])} found):")
        for footnote_num, ref in anomalies['missing_spaces']:
            print(f"   Footnote {footnote_num}: {ref}")
        
        print(f"\n2. References with 'With' prefix ({len(anomalies['with_prefix'])} found):")
        for footnote_num, ref in anomalies['with_prefix']:
            print(f"   Footnote {footnote_num}: {ref}")
        
        print(f"\n3. Incomplete references ({len(anomalies['incomplete_refs'])} found):")
        for footnote_num, ref in anomalies['incomplete_refs']:
            print(f"   Footnote {footnote_num}: {ref}")
        
        print(f"\n4. Unusual numbers in text ({len(anomalies['unusual_numbers'])} found):")
        for line_num, num, text in anomalies['unusual_numbers'][:10]:  # Show first 10
            print(f"   Line {line_num}, Number {num}: {text}...")
        
        # Show specific examples from bold text analysis
        print("\n=== BOLD TEXT ANALYSIS EXAMPLES ===")
        
        # Analyze first few pages for bold text patterns
        for page_num in range(start_page, start_page + 3):
            page = pdf.pages[page_num]
            chars = page.chars
            
            # Find bold characters
            bold_chars = [c for c in chars if 'Bold' in c.get('fontname', '')]
            
            if bold_chars:
                bold_text = ''.join([c['text'] for c in bold_chars])
                
                # Look for specific patterns
                missing_space_examples = re.findall(r'([A-Z][a-z]+)(\d+:\d+)', bold_text)
                with_prefix_examples = re.findall(r'With\s+([A-Z][a-zA-Z\s]+(?:\d+)?\s*:\s*\d+(?:-\d+)?)', bold_text)
                
                if missing_space_examples:
                    print(f"Page {page_num + 1} - Missing spaces:")
                    for book, verses in missing_space_examples:
                        print(f"  {book}{verses}")
                
                if with_prefix_examples:
                    print(f"Page {page_num + 1} - With prefix:")
                    for ref in with_prefix_examples:
                        print(f"  With {ref}")

if __name__ == "__main__":
    identify_footnote_anomalies() 