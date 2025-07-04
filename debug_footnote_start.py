#!/usr/bin/env python3
"""
Print the first 40 lines of pages 31 and 32 to see where the footnotes start.
"""
import fitz

def print_page_lines(pdf_path, page_nums, num_lines=40):
    doc = fitz.open(pdf_path)
    for page_num in page_nums:
        page = doc[page_num]
        text = page.get_text()
        lines = text.splitlines()
        print(f"\n--- Page {page_num+1} (marker should be ({page_num-30+15})) ---")
        for i, line in enumerate(lines[:num_lines]):
            print(f"{i+1:2}: {line}")
    doc.close()

if __name__ == "__main__":
    # Pages are 0-indexed; page 31 is index 30, page 32 is index 31
    print_page_lines("sources/Shorter_Catechism.pdf", [30, 31], 40) 