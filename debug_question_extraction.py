import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"

def debug_question_extraction():
    doc = fitz.open(PDF_PATH)
    
    # Count questions on each page
    page_questions = {}
    
    for page_num in range(2, 41):  # pages 3-41
        page = doc[page_num]
        text_dict = page.get_text("dict")
        questions_on_page = []
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    line_text = ""
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_size = span.get('size', 0)
                        
                        # Skip page numbers
                        if text.isdigit() and font_size >= 9.5:
                            continue
                        
                        line_text += text + " "
                    
                    line_text = line_text.strip()
                    if not line_text:
                        continue
                    
                    # Check if this is a question
                    question_match = re.match(r'^Q\.\s*(\d+)\.\s*(.+)$', line_text)
                    if question_match:
                        question_num = int(question_match.group(1))
                        questions_on_page.append(question_num)
        
        if questions_on_page:
            page_questions[page_num + 1] = questions_on_page
    
    # Print summary
    total_questions = sum(len(qs) for qs in page_questions.values())
    print(f"Total questions found: {total_questions}")
    
    print("\nQuestions by page:")
    for page_num in sorted(page_questions.keys()):
        questions = page_questions[page_num]
        print(f"  Page {page_num}: {questions}")
    
    # Check for missing questions
    all_question_nums = []
    for questions in page_questions.values():
        all_question_nums.extend(questions)
    
    all_question_nums.sort()
    print(f"\nAll question numbers: {all_question_nums}")
    
    # Check for gaps
    expected_range = range(1, 197)  # Q1-Q196
    missing_questions = [q for q in expected_range if q not in all_question_nums]
    if missing_questions:
        print(f"Missing questions: {missing_questions}")

if __name__ == "__main__":
    debug_question_extraction() 