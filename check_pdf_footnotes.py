import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"

def check_pdf_footnotes():
    doc = fitz.open(PDF_PATH)
    
    # Collect all footnote numbers from the PDF
    all_footnotes = set()
    
    for page_num in range(2, 41):  # pages 3-41
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_size = span.get('size', 0)
                        
                        # Look for footnote numbers (smaller font, 8.4pt)
                        if text.isdigit() and font_size < 9.0:
                            footnote_num = int(text)
                            if 1 <= footnote_num <= 1303:
                                all_footnotes.add(footnote_num)
    
    # Check the 864-909 range specifically
    expected_range = set(range(864, 910))
    found_in_range = all_footnotes.intersection(expected_range)
    missing_in_range = expected_range - all_footnotes
    
    print(f"Total unique footnotes found in PDF: {len(all_footnotes)}")
    print(f"Footnote range in PDF: {min(all_footnotes)} - {max(all_footnotes)}")
    
    print(f"\nExpected footnotes 864-909: {len(expected_range)}")
    print(f"Found footnotes 864-909: {len(found_in_range)}")
    print(f"Missing footnotes 864-909: {len(missing_in_range)}")
    
    if found_in_range:
        print(f"Found footnotes: {sorted(found_in_range)}")
    if missing_in_range:
        print(f"Missing footnotes: {sorted(missing_in_range)}")
    
    # Check if there are any gaps in the overall sequence
    all_footnotes_list = sorted(all_footnotes)
    gaps = []
    for i in range(len(all_footnotes_list) - 1):
        if all_footnotes_list[i+1] - all_footnotes_list[i] > 1:
            gap_start = all_footnotes_list[i] + 1
            gap_end = all_footnotes_list[i+1] - 1
            gaps.append((gap_start, gap_end))
    
    if gaps:
        print(f"\nGaps in footnote sequence:")
        for gap_start, gap_end in gaps[:10]:  # Show first 10 gaps
            print(f"  Missing {gap_start}-{gap_end}")
    else:
        print("\nNo gaps in footnote sequence!")

if __name__ == "__main__":
    check_pdf_footnotes() 