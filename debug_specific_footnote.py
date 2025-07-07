#!/usr/bin/env python3

import fitz
import re

def debug_specific_footnote():
    doc = fitz.open('sources/Shorter_Catechism-prts.pdf')
    
    # Extract text from pages 17-20 to see the structure
    plain_text = ""
    for page_num in range(16, 20):  # Pages 17-20 (0-indexed)
        page = doc[page_num]
        page_text = page.get_text()
        plain_text += page_text
    
    # Find footnote 1 specifically
    footnote_1_pattern = r'1\s+Psalm 86\.(.*?)(?=\n2\s+Psalm 16:5-11\.)'
    match = re.search(footnote_1_pattern, plain_text, re.DOTALL)
    
    if match:
        footnote_1_text = match.group(1)
        print("Footnote 1 content:")
        print(footnote_1_text)
        
        # Look for bold text patterns in this footnote
        print("\nLooking for bold text patterns in footnote 1:")
        
        # Extract structured data for pages 17-20
        structured_data = []
        for page_num in range(16, 20):
            page = doc[page_num]
            page_dict = page.get_text("dict")
            structured_data.append({
                'page': page_num,
                'blocks': page_dict.get('blocks', [])
            })
        
        # Find bold spans that might be in footnote 1
        bold_spans = []
        for page_data in structured_data:
            for block in page_data['blocks']:
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        flags = span.get('flags', 0)
                        if flags & 16:  # Bold flag
                            text = span.get('text', '')
                            if any(ref in text for ref in ['Psalm', 'Isaiah', 'Romans', '1 Corinthians', 'Revelation']):
                                bold_spans.append({
                                    'text': text,
                                    'font': span.get('font', ''),
                                    'size': span.get('size', 0),
                                    'flags': flags
                                })
        
        print(f"Found {len(bold_spans)} relevant bold spans:")
        for i, span in enumerate(bold_spans):
            print(f"  {i+1}: '{span['text']}' (font={span['font']}, size={span['size']}, flags={span['flags']})")
        
        # Try to extract references from the plain text
        print("\nExtracting references from plain text:")
        ref_pattern = r'([A-Z][a-z]+(?:\s+\d+:\d+(?:-\d+)?(?:,\s*\d+(?::\d+)?)*)?)\.'
        references = re.findall(ref_pattern, footnote_1_text)
        print(f"Found references: {references}")
        
    else:
        print("Could not find footnote 1")
    
    doc.close()

if __name__ == "__main__":
    debug_specific_footnote() 