import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"

def debug_page_ranges():
    doc = fitz.open(PDF_PATH)
    
    # First pass: collect all questions and their page ranges
    question_pages = {}
    current_question = None
    
    for page_num in range(2, 41):  # pages 3-41
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    line_text = ""
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_size = span.get('size', 0)
                        
                        # Skip page numbers (larger font)
                        if text.isdigit() and font_size >= 9.5:
                            continue
                        
                        line_text += text + " "
                    
                    line_text = line_text.strip()
                    if not line_text:
                        continue
                    
                    # Check if this is a question
                    question_match = re.match(r'^Q\.\s*(\d+)\.\s*(.+)$', line_text)
                    if question_match:
                        # Save previous question page range
                        if current_question is not None:
                            question_pages[current_question] = (question_pages[current_question][0], page_num - 1)
                            print(f"Q{current_question}: pages {question_pages[current_question][0]}-{question_pages[current_question][1]}")
                        
                        # Start new question
                        question_num = int(question_match.group(1))
                        current_question = question_num
                        question_pages[question_num] = (page_num, None)
    
    # Set end page for last question
    if current_question is not None:
        question_pages[current_question] = (question_pages[current_question][0], 40)
        print(f"Q{current_question}: pages {question_pages[current_question][0]}-{question_pages[current_question][1]}")
    
    print(f"\nTotal questions with page ranges: {len(question_pages)}")
    
    # Check for questions with very large page ranges
    large_ranges = [(q, start, end) for q, (start, end) in question_pages.items() if end - start > 5]
    if large_ranges:
        print(f"\nQuestions with large page ranges:")
        for q, start, end in large_ranges[:10]:
            print(f"  Q{q}: pages {start}-{end} ({end-start+1} pages)")

if __name__ == "__main__":
    debug_page_ranges() 