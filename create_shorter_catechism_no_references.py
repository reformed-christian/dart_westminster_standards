#!/usr/bin/env python3
"""
Create Westminster Shorter Catechism no-references JSON file
Extracts from pages 3-16 of the PDF and follows the exact format of the larger catechism no-references file.
"""

import fitz
import json
import re
from typing import List, Dict, Optional

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def extract_shorter_catechism_no_references(pdf_path: str) -> List[Dict]:
    """
    Extract Westminster Shorter Catechism from pages 3-16 (PDF pages 2-15)
    Returns format matching larger catechism no-references
    """
    doc = fitz.open(pdf_path)
    questions = []
    current_question = None
    current_answer = ""
    current_spans = []
    
    # Process pages 3-16 (PDF pages 2-15, 0-indexed)
    for page_num in range(2, 16):
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    line_text = ""
                    line_spans = []
                    
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        font_size = span.get("size", 0)
                        font_name = span.get("font", "")
                        
                        # Skip page numbers (larger font)
                        if text.isdigit() and font_size >= 9.5:
                            continue
                        
                        line_spans.append({
                            "text": text,
                            "font_size": font_size,
                            "font_name": font_name
                        })
                        line_text += text + " "
                    
                    line_text = clean_text(line_text)
                    if not line_text:
                        continue
                    
                    # Check if this is a question
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
                            'number': question_num,
                            'question': clean_text(question_text),
                            'answer': '',
                            'clauses': []
                        }
                        current_answer = ""
                        current_spans = []
                    elif current_question is not None:
                        # This is part of the answer
                        current_answer += " " + line_text
                        current_spans.extend(line_spans)
    
    # Save the last question
    if current_question is not None:
        # Extract clauses from collected spans
        clauses = extract_clauses_from_spans(current_spans)
        current_question['answer'] = clean_text(current_answer)
        current_question['clauses'] = clauses
        questions.append(current_question)
    
    doc.close()
    return questions

def extract_clauses_from_spans(spans: List[Dict]) -> List[Dict]:
    """Extract clauses from spans, splitting at footnote numbers"""
    clauses = []
    current_clause = ""
    current_footnote = None
    
    for i, span in enumerate(spans):
        text = span['text']
        font_size = span['font_size']
        
        # Check if this is a footnote number (smaller font, typically < 9.0pt)
        if text.isdigit() and font_size < 9.0:
            # This is a footnote number - assign it to the current clause
            current_footnote = int(text)
            
            # Save the current clause with this footnote number
            if current_clause.strip():
                clauses.append({
                    'text': clean_text(current_clause),
                    'footnote': current_footnote
                })
            
            # Start new clause
            current_clause = ""
        else:
            # Add to current clause
            current_clause += " " + text
    
    # Save last clause if it has content
    if current_clause.strip():
        clauses.append({
            'text': clean_text(current_clause),
            'footnote': current_footnote
        })
    
    return clauses

def clean_questions(questions: List[Dict]) -> List[Dict]:
    """Clean up questions by removing 'A.' prefix, footnote numbers from answers, and fixing clause structure"""
    cleaned_questions = []
    
    for question in questions:
        # Remove 'A.' prefix from answer
        answer = question['answer']
        if answer.startswith('A.'):
            answer = answer[2:].strip()
        # Remove footnote numbers (e.g., ' 1', ' 23', etc.) from answer
        answer = re.sub(r'\s+\d+(?=\s|$)', '', answer)
        answer = clean_text(answer)
        
        # Clean up clauses
        cleaned_clauses = []
        for clause in question['clauses']:
            text = clause['text']
            footnote = clause['footnote']
            
            # Remove 'A.' prefix from clause text
            if text.startswith('A.'):
                text = text[2:].strip()
            
            # Clean up the text
            text = clean_text(text)
            
            cleaned_clauses.append({
                'text': text,
                'footnote': footnote
            })
        
        cleaned_questions.append({
            'number': question['number'],
            'question': question['question'],
            'answer': answer,
            'clauses': cleaned_clauses
        })
    
    return cleaned_questions

def main():
    """Main function to extract and save the shorter catechism"""
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    output_path = "assets/catechisms/shorter/westminster_shorter_catechism_no_references.json"
    
    print("Extracting Westminster Shorter Catechism from pages 3-16...")
    questions = extract_shorter_catechism_no_references(pdf_path)
    
    # Clean up the questions
    questions = clean_questions(questions)
    
    # Count total clauses
    total_clauses = sum(len(q['clauses']) for q in questions)
    print(f"Extracted {len(questions)} questions with {total_clauses} total clauses")
    
    # Check questions with zero clauses
    zero_clause_questions = [q for q in questions if len(q['clauses']) == 0]
    if zero_clause_questions:
        print(f"Questions with zero clauses: {[q['number'] for q in zero_clause_questions]}")
    
    # Check questions with many clauses
    many_clause_questions = [q for q in questions if len(q['clauses']) > 20]
    if many_clause_questions:
        print(f"Questions with >20 clauses: {[(q['number'], len(q['clauses'])) for q in many_clause_questions[:5]]}")
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"Output written to: {output_path}")
    
    # Print first few questions for verification
    print(f"\nFirst 3 questions:")
    for q in questions[:3]:
        print(f"  Q{q['number']}: {len(q['clauses'])} clauses")
        for clause in q['clauses'][:2]:  # Show first 2 clauses
            print(f"    - {clause['text'][:50]}... (footnote {clause['footnote']})")

if __name__ == "__main__":
    main() 