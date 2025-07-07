#!/usr/bin/env python3
"""
Extract Westminster Shorter Catechism References - Version 3
Simple and direct approach using PyMuPDF
"""

import fitz  # PyMuPDF
import json
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path

def extract_footnotes_with_bold_text_v3():
    """Extract all footnotes with their bold scripture references using simple approach."""
    
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    output_path = "assets/catechisms/shorter/westminster_shorter_catechism_references_new.json"
    
    print("=== EXTRACTING WESTMINSTER SHORTER CATECHISM REFERENCES V3 ===")
    
    # Initialize the output structure
    footnotes = {}
    
    with fitz.open(pdf_path) as doc:
        # Start from page 17 (index 16)
        start_page = 16
        
        # Extract all text from footnote pages
        all_text = ""
        for page_num in range(start_page, len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            if page_text:
                all_text += page_text + "\n"
        
        # Process the text to identify footnotes
        lines = all_text.split('\n')
        current_footnote = None
        current_footnote_text = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and line[0].isdigit() and re.match(r'^\d+[\s:]', line):
                # This is a new footnote
                if current_footnote:
                    # Process the previous footnote
                    references = extract_references_from_footnote(doc, current_footnote, current_footnote_text)
                    footnotes[str(current_footnote)] = references
                
                match = re.match(r'^(\d+)', line)
                if match:
                    current_footnote = int(match.group(1))
                    current_footnote_text = [line]
            elif line and current_footnote:
                # This is continuation text for current footnote
                current_footnote_text.append(line)
        
        # Process the last footnote
        if current_footnote:
            references = extract_references_from_footnote(doc, current_footnote, current_footnote_text)
            footnotes[str(current_footnote)] = references
    
    # Save the results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(footnotes, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(footnotes)} footnotes")
    print(f"Results saved to: {output_path}")
    
    return footnotes

def extract_references_from_footnote(doc, footnote_num, footnote_lines):
    """Extract references and text for a single footnote."""
    
    # Combine all lines for this footnote
    full_text = " ".join(footnote_lines)
    
    # Remove page numbers
    full_text = re.sub(r'\(\d+\)', '', full_text)
    
    # Get all bold text from the PDF that appears in this footnote
    bold_references = get_bold_references_in_text(doc, full_text)
    
    if not bold_references:
        return [{"reference": "reference not found", "text": clean_text(full_text)}]
    
    # Extract references and text
    references = []
    
    # Sort references by position in text
    bold_references.sort(key=lambda x: full_text.find(x))
    
    for i, reference in enumerate(bold_references):
        # Clean up the reference (remove trailing period)
        clean_ref = reference.rstrip('.')
        
        # Find the text that follows this reference
        ref_pos = full_text.find(reference)
        if ref_pos != -1:
            # Get text from after this reference to the next reference or end
            start_pos = ref_pos + len(reference)
            
            # Find the next reference
            next_ref_pos = len(full_text)
            for next_ref in bold_references[i+1:]:
                next_pos = full_text.find(next_ref, start_pos)
                if next_pos != -1:
                    next_ref_pos = next_pos
                    break
            
            # Extract the text
            text = full_text[start_pos:next_ref_pos].strip()
        else:
            text = ""
        
        # Clean up the text
        text = clean_text(text)
        
        references.append({
            "reference": clean_ref,
            "text": text
        })
    
    return references

def get_bold_references_in_text(doc, text):
    """Get all bold text that represents scripture references from the PDF."""
    
    bold_texts = []
    
    # Search through all pages for bold text
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
                            if bold_text and bold_text in text:
                                # Check if it looks like a scripture reference
                                if is_scripture_reference(bold_text):
                                    bold_texts.append(bold_text)
    
    # Remove duplicates
    unique_bold_texts = []
    for text in bold_texts:
        if text not in unique_bold_texts:
            unique_bold_texts.append(text)
    
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
    
    with open("diagnose_shorter_extraction_v3.py", 'w') as f:
        f.write(diagnostic_script)
    
    print("Diagnostic script created: diagnose_shorter_extraction_v3.py")

if __name__ == "__main__":
    footnotes = extract_footnotes_with_bold_text_v3()
    create_diagnostic_script() 