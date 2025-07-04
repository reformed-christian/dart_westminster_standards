#!/usr/bin/env python3
import fitz

def debug_q52():
    doc = fitz.open('sources/Larger_Catechism-prts.pdf')
    text = ""
    for page_num in range(2, 41):
        page = doc[page_num]
        text += page.get_text()
    
    lines = text.split('\n')
    q52_start = False
    q52_lines = []
    
    for line in lines:
        if 'Q. 52.' in line:
            q52_start = True
            q52_lines.append(line)
        elif q52_start and line.strip() and ('Q. 53.' in line or 'Q. 54.' in line):
            break
        elif q52_start:
            q52_lines.append(line)
    
    print("Q52 raw extracted text:")
    for i, line in enumerate(q52_lines):
        print(f"{i:2d}: {line}")
    
    doc.close()

if __name__ == "__main__":
    debug_q52() 