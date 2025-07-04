import fitz
import re

def print_any_line_with_marker(pdf_path):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        lines = page.get_text().splitlines()
        for i, line in enumerate(lines):
            if re.search(r'\(\s*1\s*\)', line):
                print(f"Page {page_num+1}, line {i+1}: {repr(line)}")
    doc.close()

if __name__ == "__main__":
    print_any_line_with_marker("sources/Shorter_Catechism.pdf") 