import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"
OUTPUT_PATH = "assets/westminster_larger_catechism_extracted.json"

def clean_text(text):
    """Clean text by removing extra whitespace and normalizing"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def extract_catechism_with_font_filtering():
    doc = fitz.open(PDF_PATH)
    questions = []
    current_question = None
    current_answer = ""
    
    # Process pages 3-41 (content pages)
    for page_num in range(2, 41):  # 0-indexed, so pages 3-41
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    line_text = ""
                    line_spans = []
                    
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_size = span.get('size', 0)
                        font_name = span.get('font', '')
                        
                        # Skip page numbers (larger font size)
                        if text.isdigit() and font_size >= 9.5:
                            continue
                        
                        line_spans.append({
                            'text': text,
                            'font_size': font_size,
                            'font_name': font_name
                        })
                        line_text += text + " "
                    
                    line_text = clean_text(line_text)
                    if not line_text:
                        continue
                    
                    # Check if this is a question (starts with Q. and a number)
                    question_match = re.match(r'^Q\.\s*(\d+)\.\s*(.+)$', line_text)
                    if question_match:
                        # Save previous question if exists
                        if current_question is not None:
                            current_question['answer'] = clean_text(current_answer)
                            questions.append(current_question)
                        
                        # Start new question
                        question_num = int(question_match.group(1))
                        question_text = question_match.group(2)
                        current_question = {
                            'question': question_num,
                            'question_text': clean_text(question_text),
                            'answer': '',
                            'clauses': []
                        }
                        current_answer = ""
                    elif current_question is not None:
                        # This is part of the answer
                        current_answer += " " + line_text
    
    # Save last question
    if current_question is not None:
        current_question['answer'] = clean_text(current_answer)
        questions.append(current_question)
    
    # Now extract clauses from answers using font size filtering
    for question in questions:
        question['clauses'] = extract_clauses_from_answer(question['answer'], question['question'])
    
    return questions

def extract_clauses_from_answer(answer, question_num):
    """Extract clauses from answer text, splitting at footnote numbers (8.4pt font)"""
    doc = fitz.open(PDF_PATH)
    clauses = []
    
    # Find the page containing this question
    question_page = None
    for page_num in range(2, 41):
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    line_text = ""
                    for span in line.get('spans', []):
                        line_text += span.get('text', '')
                    
                    if f"Q. {question_num}." in line_text:
                        question_page = page_num
                        break
                if question_page is not None:
                    break
        if question_page is not None:
            break
    
    if question_page is None:
        return []
    
    # Extract the answer text with font information
    page = doc[question_page]
    text_dict = page.get_text("dict")
    
    answer_spans = []
    found_question = False
    
    for block in text_dict.get('blocks', []):
        if block.get('type') == 0:
            for line in block.get('lines', []):
                line_text = ""
                for span in line.get('spans', []):
                    line_text += span.get('text', '')
                
                # Check if we found the question
                if f"Q. {question_num}." in line_text:
                    found_question = True
                    continue
                
                # If we found the question, start collecting answer spans
                if found_question:
                    # Check if we hit the next question
                    if re.match(r'^Q\.\s*\d+\.', line_text):
                        break
                    
                    # Collect spans for this line
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_size = span.get('size', 0)
                        font_name = span.get('font', '')
                        
                        # Skip page numbers (larger font)
                        if text.isdigit() and font_size >= 9.5:
                            continue
                        
                        answer_spans.append({
                            'text': text,
                            'font_size': font_size,
                            'font_name': font_name
                        })
    
    # Process spans to extract clauses
    current_clause = ""
    current_footnote = None
    
    for i, span in enumerate(answer_spans):
        text = span['text']
        font_size = span['font_size']
        
        # Check if this is a footnote number (smaller font, 8.4pt)
        if text.isdigit() and font_size < 9.0:
            # Save previous clause if exists
            if current_clause.strip():
                clauses.append({
                    'text': clean_text(current_clause),
                    'footnote': current_footnote
                })
            
            # Start new clause
            current_footnote = int(text)
            current_clause = ""
        else:
            # Add to current clause
            current_clause += " " + text
    
    # Save last clause
    if current_clause.strip():
        clauses.append({
            'text': clean_text(current_clause),
            'footnote': current_footnote
        })
    
    return clauses

if __name__ == "__main__":
    print(f"Extracting catechism from {PDF_PATH} with font filtering...")
    questions = extract_catechism_with_font_filtering()
    
    # Count total clauses
    total_clauses = sum(len(q['clauses']) for q in questions)
    print(f"Extracted {len(questions)} questions with {total_clauses} total clauses")
    
    # Check questions with zero clauses
    zero_clause_questions = [q for q in questions if len(q['clauses']) == 0]
    if zero_clause_questions:
        print(f"Questions with zero clauses: {[q['question'] for q in zero_clause_questions]}")
    
    # Save to file
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"Output written to: {OUTPUT_PATH}") 