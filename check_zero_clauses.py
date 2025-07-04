#!/usr/bin/env python3
import fitz
import re

def check_zero_clauses():
    doc = fitz.open('sources/Larger_Catechism-prts.pdf')
    text = ""
    for page_num in range(2, 41):
        page = doc[page_num]
        text += page.get_text()
    
    lines = text.split('\n')
    
    for num in [100, 161, 188]:
        print(f"\n=== Q{num} ===")
        found = False
        for i, line in enumerate(lines):
            if f'Q. {num}.' in line:
                found = True
                print(f"Question: {line}")
                # Look for the answer
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip() and 'Q.' in lines[j]:
                        break
                    if 'A.' in lines[j]:
                        print(f"Answer: {lines[j]}")
                        # Check for numbers in the answer
                        answer_text = lines[j]
                        for k in range(j+1, min(j+10, len(lines))):
                            if lines[k].strip() and 'Q.' in lines[k]:
                                break
                            answer_text += " " + lines[k]
                        numbers = re.findall(r'\b(\d{1,4})\b', answer_text)
                        print(f"Numbers found: {numbers}")
                        break
                break
        if not found:
            print(f"Q{num} not found!")
    
    doc.close()

if __name__ == "__main__":
    check_zero_clauses() 