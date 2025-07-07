#!/usr/bin/env python3
"""
Complete extraction script for Westminster Shorter Catechism
Extracts questions, answers, clauses, footnotes, and proof texts from PDF
"""

import fitz  # PyMuPDF
import json
import re
from collections import defaultdict

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF with page information"""
    doc = fitz.open(pdf_path)
    pages = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        pages.append({
            'page': page_num + 1,
            'text': text
        })
    
    doc.close()
    return pages

def find_question_boundaries(pages):
    """Find the start and end of the Shorter Catechism questions"""
    start_page = None
    end_page = None
    
    for page in pages:
        text = page['text']
        page_num = page['page']
        
        # Look for the start of questions
        if "Q. 1. What is the chief end of man?" in text:
            start_page = page_num
            print(f"Found start of questions on page {start_page}")
        
        # Look for the end of questions
        if "Q. 107. What doth the conclusion of the Lord's Prayer teach us?" in text:
            end_page = page_num
            print(f"Found end of questions on page {end_page}")
            break
    
    return start_page, end_page

def extract_questions_and_answers(pages, start_page, end_page):
    """Extract all questions and answers from the specified pages"""
    questions = []
    current_question = None
    current_answer = ""
    
    for page in pages:
        if page['page'] < start_page or page['page'] > end_page:
            continue
            
        text = page['text']
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for question pattern
            question_match = re.match(r'Q\.\s*(\d+)\.\s*(.+)', line)
            if question_match:
                # Save previous question if exists
                if current_question:
                    current_question['answer'] = current_answer.strip()
                    questions.append(current_question)
                
                # Start new question
                question_num = int(question_match.group(1))
                question_text = question_match.group(2).strip()
                current_question = {
                    'number': question_num,
                    'question': question_text,
                    'answer': '',
                    'clauses': []
                }
                current_answer = ""
                continue
            
            # Check for answer pattern
            answer_match = re.match(r'A\.\s*(.+)', line)
            if answer_match and current_question:
                current_answer = answer_match.group(1).strip()
                continue
            
            # If we have a current question and answer, this might be continuation
            if current_question and current_answer:
                # Check if this line continues the answer
                if not re.match(r'^\d+\.', line) and not line.startswith('Q.'):
                    current_answer += " " + line
    
    # Add the last question
    if current_question:
        current_question['answer'] = current_answer.strip()
        questions.append(current_question)
    
    return questions

def extract_footnotes(pages, end_page):
    """Extract footnotes from the pages after the questions"""
    footnotes = []
    in_footnotes = False
    
    for page in pages:
        if page['page'] <= end_page:
            continue
            
        text = page['text']
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for start of footnotes
            if "FOOTNOTES" in line.upper() or "REFERENCES" in line.upper():
                in_footnotes = True
                continue
            
            if not in_footnotes:
                continue
            
            # Check for footnote number pattern
            footnote_match = re.match(r'(\d+)\.\s*(.+)', line)
            if footnote_match:
                footnote_num = int(footnote_match.group(1))
                content = footnote_match.group(2).strip()
                
                footnotes.append({
                    'footnote_num': footnote_num,
                    'content': content
                })
            elif footnotes and line:
                # Continue previous footnote
                footnotes[-1]['content'] += " " + line
    
    return footnotes

def split_into_clauses(answer_text):
    """Split answer text into clauses based on footnote numbers"""
    clauses = []
    
    # Pattern to match text followed by footnote numbers
    # This handles cases like "text,1 and more text2"
    pattern = r'([^0-9]+?)(\d+)'
    matches = list(re.finditer(pattern, answer_text))
    
    if not matches:
        # No footnotes found, treat as single clause
        clauses.append({
            'text': answer_text.strip(),
            'footnoteNum': None,
            'proofTexts': []
        })
        return clauses
    
    # Process each match
    for i, match in enumerate(matches):
        text = match.group(1).strip()
        footnote_num = int(match.group(2))
        
        # Clean up the text
        text = re.sub(r'[,\s]+$', '', text)  # Remove trailing commas and spaces
        
        clauses.append({
            'text': text,
            'footnoteNum': footnote_num,
            'proofTexts': []
        })
    
    return clauses

def clean_answer_text(answer_text):
    """Clean answer text by removing footnote numbers"""
    # Remove footnote numbers from the answer text
    cleaned = re.sub(r'\d+', '', answer_text)
    # Clean up extra spaces and punctuation
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'[,\s]+$', '', cleaned)
    return cleaned.strip()

def add_proof_texts_to_clauses(clauses, footnotes):
    """Add proof texts to clauses based on footnote content"""
    footnote_dict = {f['footnote_num']: f['content'] for f in footnotes}
    
    for clause in clauses:
        if clause['footnoteNum'] and clause['footnoteNum'] in footnote_dict:
            content = footnote_dict[clause['footnoteNum']]
            
            # Parse proof texts from footnote content
            proof_texts = parse_proof_texts(content)
            clause['proofTexts'] = proof_texts

def parse_proof_texts(content):
    """Parse proof texts from footnote content"""
    proof_texts = []
    
    # Split by common separators
    parts = re.split(r'\s+(?=[A-Z][a-z]+\s+\d+:)', content)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Look for reference pattern
        ref_match = re.match(r'([A-Za-z]+\s+\d+:[^.]*\.?)(.+)', part)
        if ref_match:
            reference = ref_match.group(1).strip()
            text = ref_match.group(2).strip()
            
            proof_texts.append({
                'reference': reference,
                'text': text
            })
        else:
            # If no clear reference pattern, treat as continuation
            if proof_texts:
                proof_texts[-1]['text'] += " " + part
            else:
                # Fallback: treat as single proof text
                proof_texts.append({
                    'reference': 'Unknown',
                    'text': part
                })
    
    return proof_texts

def create_final_structure(questions, footnotes):
    """Create the final JSON structure"""
    # Process each question
    for question in questions:
        # Clean the answer text
        question['answer'] = clean_answer_text(question['answer'])
        
        # Split into clauses
        clauses = split_into_clauses(question['answer'])
        question['clauses'] = clauses
        
        # Add proof texts to clauses
        add_proof_texts_to_clauses(clauses, footnotes)
    
    # Create the final structure
    result = {
        "title": "Westminster Shorter Catechism",
        "year": 1647,
        "questions": questions,
        "footnotes": footnotes
    }
    
    return result

def main():
    """Main extraction function"""
    print("Extracting Westminster Shorter Catechism...")
    
    # Extract text from PDF
    pages = extract_text_from_pdf('sources/Shorter_Catechism.pdf')
    print(f"Extracted {len(pages)} pages")
    
    # Find question boundaries
    start_page, end_page = find_question_boundaries(pages)
    if not start_page or not end_page:
        print("Could not find question boundaries")
        return
    
    print(f"Questions span from page {start_page} to {end_page}")
    
    # Extract questions and answers
    questions = extract_questions_and_answers(pages, start_page, end_page)
    print(f"Extracted {len(questions)} questions")
    
    # Extract footnotes
    footnotes = extract_footnotes(pages, end_page)
    print(f"Extracted {len(footnotes)} footnotes")
    
    # Create final structure
    result = create_final_structure(questions, footnotes)
    
    # Save to file
    output_file = 'assets/catechisms/shorter/westminster_shorter_catechism_complete.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Saved complete extraction to {output_file}")
    
    # Print summary
    total_clauses = sum(len(q['clauses']) for q in questions)
    total_proof_texts = sum(len(c['proofTexts']) for q in questions for c in q['clauses'])
    
    print(f"\nExtraction Summary:")
    print(f"Questions: {len(questions)}")
    print(f"Clauses: {total_clauses}")
    print(f"Footnotes: {len(footnotes)}")
    print(f"Proof texts: {total_proof_texts}")

if __name__ == "__main__":
    main() 