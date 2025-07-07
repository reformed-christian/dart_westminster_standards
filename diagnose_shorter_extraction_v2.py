#!/usr/bin/env python3
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
    print("\n=== SAMPLE FOOTNOTES ===")
    for i in range(1, 6):
        if str(i) in footnotes:
            print(f"Footnote {i}:")
            for ref in footnotes[str(i)]:
                print(f"  Reference: {ref['reference']}")
                print(f"  Text: {ref['text'][:100]}...")
                print()

if __name__ == "__main__":
    diagnose_extraction()
