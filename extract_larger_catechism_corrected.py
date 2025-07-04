import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"
OUTPUT_PATH = "assets/westminster_larger_catechism_corrected.json"

def clean_text(text):
    """Clean text by removing extra whitespace and normalizing"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_catechism_corrected():
    doc = fitz.open(PDF_PATH)
    questions = []
    
    # Process pages 3-41 (content pages only)
    for page_num in range(2, 41):  # 0-indexed, so pages 3-41
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        current_question = None
        current_answer = ""
        current_spans = []
        
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
                            # Extract clauses from collected spans
                            clauses = extract_clauses_from_spans(current_spans)
                            current_question['answer'] = clean_text(current_answer)
                            current_question['clauses'] = clauses
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
                        current_spans = []
                    elif current_question is not None:
                        # This is part of the answer
                        current_answer += " " + line_text
                        current_spans.extend(line_spans)
        
        # Save question if it spans to the end of the page
        if current_question is not None:
            # Extract clauses from collected spans
            clauses = extract_clauses_from_spans(current_spans)
            current_question['answer'] = clean_text(current_answer)
            current_question['clauses'] = clauses
            questions.append(current_question)
    
    return questions

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

if __name__ == "__main__":
    print(f"Extracting catechism from {PDF_PATH} (pages 3-41 only)...")
    questions = extract_catechism_corrected()
    
    # Count total clauses
    total_clauses = sum(len(q['clauses']) for q in questions)
    print(f"Extracted {len(questions)} questions with {total_clauses} total clauses")
    
    # Check questions with zero clauses
    zero_clause_questions = [q for q in questions if len(q['clauses']) == 0]
    if zero_clause_questions:
        print(f"Questions with zero clauses: {[q['question'] for q in zero_clause_questions]}")
    
    # Check questions with many clauses
    many_clause_questions = [q for q in questions if len(q['clauses']) > 30]
    if many_clause_questions:
        print(f"Questions with >30 clauses: {[(q['question'], len(q['clauses'])) for q in many_clause_questions[:5]]}")
    
    # Verify we're not going past page 41
    print(f"Processing limited to pages 3-41 (PDF pages 2-40 in 0-indexed)")
    
    # Save to file
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"Output written to: {OUTPUT_PATH}") 