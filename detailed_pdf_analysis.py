#!/usr/bin/env python3
"""
Detailed PDF Analysis for Westminster Shorter Catechism
Analyzes the exact structure of footnotes and identifies parsing challenges
"""

import pdfplumber
import json
import re
from pathlib import Path
from typing import Dict, List, Any

def analyze_footnote_structure():
    """Analyze the exact structure of footnotes to understand parsing requirements."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("=== DETAILED FOOTNOTE STRUCTURE ANALYSIS ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Start from page 17 (index 16)
        start_page = 16
        
        # Analyze first few footnotes in detail
        for page_num in range(start_page, start_page + 3):  # Pages 17-19
            page = pdf.pages[page_num]
            print(f"\n--- DETAILED ANALYSIS OF PAGE {page_num + 1} ---")
            
            # Extract characters with their properties
            chars = page.chars
            print(f"Total characters: {len(chars)}")
            
            # Group by font
            fonts = {}
            for char in chars:
                font_name = char.get('fontname', 'unknown')
                if font_name not in fonts:
                    fonts[font_name] = []
                fonts[font_name].append(char)
            
            print(f"Fonts found: {len(fonts)}")
            for font_name, chars_list in fonts.items():
                print(f"  {font_name}: {len(chars_list)} characters")
                
                # Show first 100 characters from each font
                sample_text = ''.join([c['text'] for c in chars_list[:100]])
                print(f"    Sample: {sample_text}")
                
                # Show character properties for first few characters
                if chars_list:
                    first_char = chars_list[0]
                    print(f"    First char properties: {first_char}")
            
            # Look for bold text specifically
            bold_chars = [c for c in chars if 'Bold' in c.get('fontname', '')]
            if bold_chars:
                print(f"\nBold characters found: {len(bold_chars)}")
                bold_text = ''.join([c['text'] for c in bold_chars])
                print(f"Bold text: {bold_text}")
                
                # Analyze bold text structure
                print("\nBold text analysis:")
                current_ref = ""
                for char in bold_chars:
                    if char['text'].isalpha() or char['text'].isdigit() or char['text'] in '.:':
                        current_ref += char['text']
                    else:
                        if current_ref.strip():
                            print(f"  Reference: '{current_ref.strip()}'")
                            current_ref = ""
                
                if current_ref.strip():
                    print(f"  Reference: '{current_ref.strip()}'")
            
            # Look for superscript numbers (footnote markers)
            small_chars = [c for c in chars if c.get('size', 0) < 12]
            if small_chars:
                print(f"\nSmall characters found: {len(small_chars)}")
                small_text = ''.join([c['text'] for c in small_chars])
                print(f"Small text: {small_text}")
            
            print("-" * 80)

def analyze_footnote_patterns():
    """Analyze the patterns in footnotes to understand how to parse them."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== FOOTNOTE PATTERN ANALYSIS ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from pages 17-20 to analyze patterns
        all_text = ""
        for page_num in range(16, 20):  # Pages 17-20
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
        
        # Look for footnote patterns
        lines = all_text.split('\n')
        
        # Find lines that start with numbers (potential footnotes)
        footnote_lines = []
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit():
                # Check if it looks like a footnote (number followed by book name)
                if re.match(r'^\d+\s+[A-Z]', line):
                    footnote_lines.append((i, line))
        
        print(f"Found {len(footnote_lines)} potential footnote lines")
        
        # Analyze first 10 footnotes
        for i, (line_num, line) in enumerate(footnote_lines[:10]):
            print(f"\nFootnote {i+1} (line {line_num}):")
            print(f"  Text: {line[:200]}...")
            
            # Try to identify scripture references
            # Look for patterns like "Book Name 1:2-3"
            ref_pattern = r'([A-Z][a-zA-Z\s]+(?:\d+)?)\s*:\s*(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)'
            matches = re.finditer(ref_pattern, line)
            
            refs_found = []
            for match in matches:
                book = match.group(1).strip()
                verses = match.group(2).strip()
                ref = f"{book}:{verses}"
                refs_found.append(ref)
            
            if refs_found:
                print(f"  References found: {refs_found}")
            else:
                print(f"  No clear references found")

def identify_anomalies():
    """Identify potential anomalies or challenges in the PDF structure."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== ANOMALY IDENTIFICATION ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Check for potential issues across all footnote pages
        issues = []
        
        for page_num in range(16, len(pdf.pages)):  # Pages 17 onwards
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            
            if not page_text:
                issues.append(f"Page {page_num + 1}: No text extracted")
                continue
            
            # Look for page numbers that might interfere
            page_numbers = re.findall(r'\(\d+\)', page_text)
            if page_numbers:
                issues.append(f"Page {page_num + 1}: Contains page numbers {page_numbers}")
            
            # Look for unusual patterns
            lines = page_text.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Check for lines that start with numbers but don't look like footnotes
                if line and line[0].isdigit():
                    if not re.match(r'^\d+\s+[A-Z]', line):
                        issues.append(f"Page {page_num + 1}, Line {i}: Unusual number pattern: {line[:50]}")
                
                # Check for very long lines (might indicate formatting issues)
                if len(line) > 200:
                    issues.append(f"Page {page_num + 1}, Line {i}: Very long line ({len(line)} chars)")
        
        if issues:
            print("Potential issues found:")
            for issue in issues[:20]:  # Show first 20 issues
                print(f"  {issue}")
        else:
            print("No obvious issues found")

def test_scripture_extraction():
    """Test extraction of scripture references from a sample footnote."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    
    print("\n=== SCRIPTURE EXTRACTION TEST ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        # Focus on page 17 (first footnote page)
        page = pdf.pages[16]
        chars = page.chars
        
        # Find bold characters (scripture references)
        bold_chars = [c for c in chars if 'Bold' in c.get('fontname', '')]
        
        if bold_chars:
            print(f"Found {len(bold_chars)} bold characters")
            
            # Group bold characters into words
            bold_text = ''.join([c['text'] for c in bold_chars])
            print(f"Complete bold text: {bold_text}")
            
            # Try to parse scripture references
            # Look for patterns like "Psalm 86." or "Isaiah 60:21."
            ref_pattern = r'([A-Z][a-zA-Z\s]+(?:\d+)?)\s*:\s*(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\.?'
            matches = re.finditer(ref_pattern, bold_text)
            
            print("\nExtracted references:")
            for match in matches:
                book = match.group(1).strip()
                verses = match.group(2).strip()
                ref = f"{book}:{verses}"
                print(f"  {ref}")
        else:
            print("No bold characters found")

if __name__ == "__main__":
    analyze_footnote_structure()
    analyze_footnote_patterns()
    identify_anomalies()
    test_scripture_extraction() 