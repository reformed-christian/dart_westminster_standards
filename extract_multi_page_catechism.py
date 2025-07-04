import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"
OUTPUT_PATH = "assets/westminster_larger_catechism_multi_page.json"

def clean_text(text):
    """Clean text by removing extra whitespace and normalizing"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_multi_page_catechism():
    doc = fitz.open(PDF_PATH)
    questions = []
    
    # First pass: collect all questions and their complete page ranges
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
                    
                    line_text = clean_text(line_text)
                    if not line_text:
                        continue
                    
                    # Check if this is a question
                    question_match = re.match(r'^Q\.\s*(\d+)\.\s*(.+)$', line_text)
                    if question_match:
                        # Save previous question page range
                        if current_question is not None:
                            question_pages[current_question] = (question_pages[current_question][0], page_num - 1)
                        
                        # Start new question
                        question_num = int(question_match.group(1))
                        current_question = question_num
                        question_pages[question_num] = (page_num, None)
    
    # Set end page for last question
    if current_question is not None:
        question_pages[current_question] = (question_pages[current_question][0], 40)
    
    # Second pass: extract each question with complete content across all its pages
    for question_num in sorted(question_pages.keys()):
        start_page, end_page = question_pages[question_num]
        
        # Ensure valid page range
        if start_page > end_page:
            end_page = start_page
        
        question_data = extract_question_multi_page(doc, question_num, start_page, end_page)
        if question_data:
            questions.append(question_data)
    
    return questions

def extract_question_multi_page(doc, question_num, start_page, end_page):
    """Extract a single question with complete content across multiple pages"""
    
    # Collect all spans for this question across all its pages
    all_spans = []
    question_text = ""
    found_question = False
    collecting_answer = False
    
    for page_num in range(start_page, end_page + 1):
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
                        
                        # Skip page numbers
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
                    
                    # Check if we found the question
                    if f"Q. {question_num}." in line_text:
                        found_question = True
                        collecting_answer = False
                        # Extract question text
                        question_match = re.match(r'^Q\.\s*(\d+)\.\s*(.+)$', line_text)
                        if question_match:
                            question_text = question_match.group(2)
                        continue
                    
                    # If we found the question, start collecting answer
                    if found_question:
                        # Check if we hit the next question
                        if re.match(r'^Q\.\s*\d+\.', line_text):
                            break
                        
                        # Start collecting answer spans
                        collecting_answer = True
                        all_spans.extend(line_spans)
    
    if not found_question:
        return None
    
    # Extract clauses from spans
    clauses = extract_clauses_from_spans(all_spans)
    
    # Build answer text
    answer_text = ""
    for span in all_spans:
        answer_text += span['text'] + " "
    answer_text = clean_text(answer_text)
    
    return {
        'question': question_num,
        'question_text': clean_text(question_text),
        'answer': answer_text,
        'clauses': clauses
    }

def extract_clauses_from_spans(spans):
    """Extract clauses from spans, splitting at footnote numbers"""
    clauses = []
    current_clause = ""
    current_footnote = None
    
    for span in spans:
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

def verify_extraction(questions):
    """Verify that we have exactly 196 questions and 1303 clauses"""
    total_questions = len(questions)
    total_clauses = sum(len(q['clauses']) for q in questions)
    
    print(f"Extracted {total_questions} questions with {total_clauses} total clauses")
    
    if total_questions != 196:
        print(f"ERROR: Expected 196 questions, got {total_questions}")
        return False
    
    # Collect all footnote numbers
    all_footnotes = []
    for q in questions:
        for clause in q['clauses']:
            if clause['footnote'] is not None:
                all_footnotes.append(clause['footnote'])
    
    unique_footnotes = len(set(all_footnotes))
    print(f"Unique footnote numbers: {unique_footnotes}")
    
    if unique_footnotes != 1303:
        print(f"ERROR: Expected 1303 unique footnotes, got {unique_footnotes}")
        return False
    
    print("SUCCESS: Extraction verified!")
    return True

if __name__ == "__main__":
    print(f"Extracting catechism with multi-page support from {PDF_PATH}...")
    questions = extract_multi_page_catechism()
    
    # Verify extraction
    if verify_extraction(questions):
        # Save to file
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"Output written to: {OUTPUT_PATH}")
    else:
        print("Extraction failed verification!") 