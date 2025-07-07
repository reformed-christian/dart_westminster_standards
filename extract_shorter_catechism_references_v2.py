#!/usr/bin/env python3
"""
Extract Westminster Shorter Catechism References - Version 2
Improved extraction using PyMuPDF with better bold text detection
"""

import fitz  # PyMuPDF
import json
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path

def extract_footnotes_with_bold_text_v2():
    """Extract all footnotes with their bold scripture references using improved PyMuPDF approach."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    output_path = "assets/catechisms/shorter/westminster_shorter_catechism_references_new.json"
    
    print("=== EXTRACTING WESTMINSTER SHORTER CATECHISM REFERENCES V2 ===")
    
    # Initialize the output structure
    footnotes = {}
    
    with fitz.open(pdf_path) as doc:
        # Start from page 17 (index 16)
        start_page = 16
        
        # First pass: identify all footnote boundaries
        footnote_boundaries = identify_footnote_boundaries(doc, start_page)
        
        # Second pass: extract each footnote individually
        for footnote_num, (start_line, end_line, page_range) in footnote_boundaries.items():
            references = extract_footnote_references(doc, footnote_num, start_line, end_line, page_range)
            footnotes[str(footnote_num)] = references
    
    # Save the results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(footnotes, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(footnotes)} footnotes")
    print(f"Results saved to: {output_path}")
    
    return footnotes

def identify_footnote_boundaries(doc, start_page):
    """Identify the boundaries of each footnote."""
    
    footnote_boundaries = {}
    current_footnote = None
    current_start_line = None
    current_page_range = []
    
    # Extract all text from footnote pages
    all_text = ""
    for page_num in range(start_page, len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        if page_text:
            all_text += page_text + "\n"
    
    lines = all_text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line and line[0].isdigit() and re.match(r'^\d+[\s:]', line):
            # This is a new footnote
            if current_footnote:
                # Save the previous footnote
                footnote_boundaries[current_footnote] = (current_start_line, i, current_page_range)
            
            match = re.match(r'^(\d+)', line)
            if match:
                current_footnote = int(match.group(1))
                current_start_line = i
                current_page_range = []
        elif line and current_footnote:
            # This is continuation text for current footnote
            pass
    
    # Save the last footnote
    if current_footnote:
        footnote_boundaries[current_footnote] = (current_start_line, len(lines), current_page_range)
    
    return footnote_boundaries

def extract_footnote_references(doc, footnote_num, start_line, end_line, page_range):
    """Extract references and text for a single footnote."""
    
    # Get the footnote text
    footnote_text = ""
    for page_num in range(16, len(doc)):  # Pages 17 onwards
        page = doc[page_num]
        page_text = page.get_text()
        if page_text:
            footnote_text += page_text + "\n"
    
    lines = footnote_text.split('\n')
    footnote_lines = lines[start_line:end_line]
    full_text = " ".join(footnote_lines)
    
    # Remove page numbers
    full_text = re.sub(r'\(\d+\)', '', full_text)
    
    # Extract bold text from the specific footnote area
    bold_references = extract_bold_text_from_footnote(doc, footnote_num, full_text)
    
    if not bold_references:
        return [{"reference": "reference not found", "text": clean_text(full_text)}]
    
    # Split text by references and extract text
    references = []
    remaining_text = full_text
    
    for reference in bold_references:
        # Clean up the reference
        clean_ref = reference.rstrip('.')
        
        # Find the text that follows this reference
        if clean_ref in remaining_text:
            # Split at the reference
            parts = remaining_text.split(clean_ref, 1)
            if len(parts) > 1:
                text = parts[1].strip()
                # Find where the next reference starts
                next_ref_start = find_next_reference_start(text, bold_references, clean_ref)
                if next_ref_start > 0:
                    text = text[:next_ref_start].strip()
                remaining_text = parts[1][next_ref_start:] if next_ref_start > 0 else ""
            else:
                text = ""
                remaining_text = ""
        else:
            text = ""
        
        # Clean up the text
        text = clean_text(text)
        
        references.append({
            "reference": clean_ref,
            "text": text
        })
    
    return references

def extract_bold_text_from_footnote(doc, footnote_num, footnote_text):
    """Extract bold text that represents scripture references from a specific footnote."""
    
    bold_texts = []
    
    # Search through all pages for bold text that appears in this footnote
    for page_num in range(16, len(doc)):  # Pages 17 onwards
        page = doc[page_num]
        
        # Get text blocks with font information
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["flags"] & 16:  # Bold flag
                            bold_text = span["text"].strip()
                            if bold_text and bold_text in footnote_text:
                                # Check if it looks like a scripture reference
                                if is_scripture_reference(bold_text):
                                    bold_texts.append(bold_text)
    
    # Remove duplicates and sort by position in text
    unique_bold_texts = []
    for text in bold_texts:
        if text not in unique_bold_texts:
            unique_bold_texts.append(text)
    
    # Sort by position in footnote text
    unique_bold_texts.sort(key=lambda x: footnote_text.find(x))
    
    return unique_bold_texts

def is_scripture_reference(text):
    """Check if text looks like a scripture reference."""
    
    # Patterns for scripture references
    patterns = [
        r'^[A-Z][a-z]+',  # Book names like "Genesis", "Matthew"
        r'^\d+\s+[A-Z]',  # Numbered books like "1 Corinthians"
        r'^[A-Z][a-z]+:\d+',  # Book:verse like "John:3"
        r'^[A-Z][a-z]+\s+\d+:\d+',  # Book chapter:verse like "John 3:16"
        r'^Cf\.',  # Cross references like "Cf."
        r'^With\s+[A-Z]',  # References with "With" prefix
    ]
    
    for pattern in patterns:
        if re.match(pattern, text):
            return True
    
    return False

def find_next_reference_start(text, all_references, current_ref):
    """Find where the next reference starts in the text."""
    
    if not all_references:
        return -1
    
    # Find the index of the current reference
    try:
        current_index = all_references.index(current_ref)
    except ValueError:
        return -1
    
    # Look for the next reference in the text
    for i in range(current_index + 1, len(all_references)):
        next_ref = all_references[i]
        pos = text.find(next_ref)
        if pos != -1:
            return pos
    
    return -1

def clean_text(text):
    """Clean up text by removing extra whitespace and page numbers."""
    
    # Remove page numbers
    text = re.sub(r'\(\d+\)', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def create_diagnostic_script():
    """Create a diagnostic script to verify the extraction."""
    
    diagnostic_script = '''#!/usr/bin/env python3
"""
Diagnostic script for Westminster Shorter Catechism References
"""

import json
import sys

def diagnose_extraction():
    """Diagnose the extraction results."""
    
    try:
        with open("assets/catechisms/shorter/westminster_shorter_catechism_references_new.json", 'r') as f:
            footnotes = json.load(f)
    except FileNotFoundError:
        print("❌ Output file not found!")
        return
    
    print("=== DIAGNOSTIC RESULTS ===")
    
    # Check total footnotes
    total_footnotes = len(footnotes)
    print(f"Total footnotes: {total_footnotes}")
    
    if total_footnotes != 227:
        print(f"❌ Expected 227 footnotes, found {total_footnotes}")
    else:
        print("✓ All 227 footnotes found!")
    
    # Check for missing footnotes
    expected_footnotes = set(range(1, 228))
    found_footnotes = set(int(k) for k in footnotes.keys())
    missing = expected_footnotes - found_footnotes
    
    if missing:
        print(f"❌ Missing footnotes: {sorted(missing)}")
    else:
        print("✓ No missing footnotes!")
    
    # Check for empty footnotes
    empty_footnotes = []
    for num, refs in footnotes.items():
        if not refs:
            empty_footnotes.append(int(num))
    
    if empty_footnotes:
        print(f"⚠️  Empty footnotes: {sorted(empty_footnotes)}")
    else:
        print("✓ No empty footnotes!")
    
    # Check for "reference not found" entries
    not_found_count = 0
    for num, refs in footnotes.items():
        for ref in refs:
            if ref.get("reference") == "reference not found":
                not_found_count += 1
                print(f"⚠️  Footnote {num}: reference not found")
    
    if not_found_count == 0:
        print("✓ All references found!")
    else:
        print(f"⚠️  Total references not found: {not_found_count}")
    
    # Check for empty text
    empty_text_count = 0
    for num, refs in footnotes.items():
        for ref in refs:
            if not ref.get("text", "").strip():
                empty_text_count += 1
                print(f"⚠️  Footnote {num}: empty text for reference '{ref.get('reference')}'")
    
    if empty_text_count == 0:
        print("✓ All references have text!")
    else:
        print(f"⚠️  Total empty text entries: {empty_text_count}")
    
    # Show sample of first few footnotes
    print("\\n=== SAMPLE FOOTNOTES ===")
    for i in range(1, 6):
        if str(i) in footnotes:
            print(f"Footnote {i}:")
            for ref in footnotes[str(i)]:
                print(f"  Reference: {ref['reference']}")
                print(f"  Text: {ref['text'][:100]}...")
                print()

if __name__ == "__main__":
    diagnose_extraction()
'''
    
    with open("diagnose_shorter_extraction_v2.py", 'w') as f:
        f.write(diagnostic_script)
    
    print("Diagnostic script created: diagnose_shorter_extraction_v2.py")

if __name__ == "__main__":
    footnotes = extract_footnotes_with_bold_text_v2()
    create_diagnostic_script() 