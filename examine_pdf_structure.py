#!/usr/bin/env python3

import fitz
import json

def examine_pdf_structure():
    doc = fitz.open('sources/Shorter_Catechism-prts.pdf')
    print(f'Total pages: {len(doc)}')
    
    # Examine page 16 (index 16) where footnotes start
    page = doc[16]
    text = page.get_text('dict')
    
    print(f'\nPage 16 structure:')
    print(f'Blocks: {len(text["blocks"])}')
    
    for i, block in enumerate(text['blocks']):
        print(f'\nBlock {i}: {len(block.get("lines", []))} lines')
        if block.get('lines'):
            for j, line in enumerate(block['lines'][:3]):  # First 3 lines
                print(f'  Line {j}: {len(line.get("spans", []))} spans')
                for k, span in enumerate(line.get('spans', [])[:3]):  # First 3 spans
                    font = span.get('font', 'N/A')
                    size = span.get('size', 'N/A')
                    flags = span.get('flags', 'N/A')
                    text_content = span.get('text', 'N/A')[:100]
                    print(f'    Span {k}: font={font}, size={size}, flags={flags}, text="{text_content}..."')
    
    # Look for bold text patterns
    print(f'\nBold text patterns on page 16:')
    bold_spans = []
    for block in text['blocks']:
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                if span.get('flags', 0) & 16:  # Bold flag
                    bold_spans.append({
                        'font': span.get('font'),
                        'size': span.get('size'),
                        'flags': span.get('flags'),
                        'text': span.get('text', '')
                    })
    
    for i, span in enumerate(bold_spans[:10]):  # First 10 bold spans
        print(f'Bold span {i}: font={span["font"]}, size={span["size"]}, flags={span["flags"]}, text="{span["text"]}"')
    
    doc.close()

if __name__ == "__main__":
    examine_pdf_structure() 