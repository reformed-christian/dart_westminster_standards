import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"
OUTPUT_PATH = "assets/westminster_larger_catechism_correct_footnotes.json"

def clean_text(text):
    """Clean text by removing extra whitespace and normalizing"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_correct_footnotes():
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

def verify_question_145(questions):
    """Verify that question 145 has footnotes 864-909"""
    q145 = None
    for q in questions:
        if q['question'] == 145:
            q145 = q
            break
    
    if not q145:
        print("ERROR: Question 145 not found!")
        return False
    
    # Extract all footnote numbers
    footnotes = []
    for clause in q145['clauses']:
        if clause['footnote'] is not None:
            footnotes.append(clause['footnote'])
    
    footnotes.sort()
    print(f"Q145 footnotes: {footnotes}")
    print(f"Q145 footnote range: {min(footnotes)} - {max(footnotes)}")
    print(f"Q145 total footnotes: {len(footnotes)}")
    
    # Check if we have the expected range 864-909
    expected_range = set(range(864, 910))  # 864 to 909 inclusive
    actual_footnotes = set(footnotes)
    
    if actual_footnotes == expected_range:
        print("✅ SUCCESS: Question 145 has correct footnotes 864-909!")
        return True
    else:
        missing = expected_range - actual_footnotes
        extra = actual_footnotes - expected_range
        print(f"❌ ERROR: Question 145 has incorrect footnote numbers")
        if missing:
            print(f"Missing footnotes: {sorted(missing)[:10]}...")
        if extra:
            print(f"Extra footnotes: {sorted(extra)[:10]}...")
        return False

if __name__ == "__main__":
    print(f"Extracting catechism with correct footnotes from {PDF_PATH}...")
    questions = extract_correct_footnotes()
    
    # Count total clauses
    total_clauses = sum(len(q['clauses']) for q in questions)
    print(f"Extracted {len(questions)} questions with {total_clauses} total clauses")
    
    # Verify question 145 specifically
    if verify_question_145(questions):
        # Save to file
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"Output written to: {OUTPUT_PATH}")
    else:
        print("Extraction failed verification for Q145!") 