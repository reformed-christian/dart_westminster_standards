#!/usr/bin/env python3
"""
Debug PDF Bold Text Detection using PyMuPDF (fitz) - Correct API usage
"""

import fitz  # PyMuPDF
import re
from pathlib import Path

def debug_bold_pymupdf(pdf_path: str):
    print(f"🔍 Checking for bold text/font info using PyMuPDF in: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    print(f"PDF has {len(doc)} pages")
    
    # Look at pages around where we expect footnotes (pages 30-35)
    for page_num in range(30, min(36, len(doc))):
        page = doc[page_num]
        print(f"\n📖 Examining PDF page {page_num+1}:")
        
        # Get text with font information using the correct API
        text_dict = page.get_text("dict")
        print(f"  Found {len(text_dict.get('blocks', []))} blocks")
        
        # Show first few lines of text
        text = page.get_text()
        lines = text.splitlines()
        print(f"  First 5 lines of text:")
        for i, line in enumerate(lines[:5]):
            print(f"    Line {i+1}: {repr(line)}")
        
        # Look for page markers
        for line in lines[-5:]:
            if re.search(r'\(\s*\d+\s*\)', line):
                print(f"    Found page marker: {repr(line)}")
        
        # Examine font information from text spans
        span_count = 0
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:  # Text block
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        font = span.get('font', 'unknown')
                        size = span.get('size', 0)
                        flags = span.get('flags', 0)
                        text = span.get('text', '')
                        
                        # Check for bold indicators
                        is_bold = False
                        bold_reasons = []
                        
                        # Check font name for bold indicators
                        if 'bold' in font.lower():
                            is_bold = True
                            bold_reasons.append('font name contains "bold"')
                        
                        # Check flags (bit 20 is often bold)
                        if flags & (1 << 20):
                            is_bold = True
                            bold_reasons.append('bold flag set')
                        
                        # Check for other common bold indicators
                        if flags & (1 << 1):
                            bold_reasons.append('italic flag set')
                        
                        print(f"    Span {span_count+1}: Font: {font} | Size: {size} | Flags: {flags} | Bold: {is_bold}")
                        print(f"      Text: {repr(text[:50])}")
                        if bold_reasons:
                            print(f"      Bold reasons: {', '.join(bold_reasons)}")
                        
                        span_count += 1
                        if span_count >= 10:  # Limit to first 10 spans
                            break
                    if span_count >= 10:
                        break
                if span_count >= 10:
                    break
        
        print("  " + "="*50)
    
    doc.close()

def main():
    pdf_path = "sources/Shorter_Catechism.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return
    debug_bold_pymupdf(pdf_path)

if __name__ == "__main__":
    main() 