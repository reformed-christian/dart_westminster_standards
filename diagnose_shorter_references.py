#!/usr/bin/env python3
"""
Diagnostic script for Westminster Shorter Catechism References
"""

import json
import sys

def diagnose_references():
    """Diagnose the extracted references."""
    
    try:
        with open("assets/catechisms/shorter/westminster_shorter_catechism_references_new.json", 'r') as f:
            footnotes = json.load(f)
    except FileNotFoundError:
        print("❌ References file not found!")
        return
    
    print("=== DIAGNOSING SHORTER CATECHISM REFERENCES ===")
    
    # Check total footnotes
    total_footnotes = len(footnotes)
    print(f"Total footnotes: {total_footnotes}")
    
    if total_footnotes != 227:
        print(f"❌ Expected 227 footnotes, found {total_footnotes}")
    else:
        print("✓ All 227 footnotes present")
    
    # Check for empty footnotes
    empty_footnotes = [num for num, refs in footnotes.items() if not refs]
    if empty_footnotes:
        print(f"Empty footnotes: {empty_footnotes}")
    else:
        print("✓ No empty footnotes")
    
    # Count total references
    total_references = sum(len(refs) for refs in footnotes.values())
    print(f"Total references: {total_references}")
    
    # Check for malformed references
    malformed = []
    for num, refs in footnotes.items():
        for ref in refs:
            if not ref.get('reference') or not ref.get('text'):
                malformed.append((num, ref))
    
    if malformed:
        print(f"Malformed references: {len(malformed)}")
        for num, ref in malformed[:5]:  # Show first 5
            print(f"  Footnote {num}: {ref}")
    else:
        print("✓ No malformed references")
    
    # Show sample of first few footnotes
    print("\nSample footnotes:")
    for i in range(1, 6):
        if str(i) in footnotes:
            refs = footnotes[str(i)]
            print(f"  Footnote {i}: {len(refs)} references")
            for ref in refs:
                print(f"    {ref['reference']}: {ref['text'][:50]}...")

if __name__ == "__main__":
    diagnose_references()
