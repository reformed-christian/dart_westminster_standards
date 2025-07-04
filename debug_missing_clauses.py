import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"

def debug_missing_clauses():
    # Load the current extraction
    with open("assets/westminster_larger_catechism_corrected.json", 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Current extraction: {len(questions)} questions, {sum(len(q['clauses']) for q in questions)} clauses")
    
    # Check if we have exactly 196 questions
    if len(questions) != 196:
        print(f"ERROR: Expected 196 questions, got {len(questions)}")
        return
    
    # Collect all footnote numbers
    all_footnotes = []
    for q in questions:
        for clause in q['clauses']:
            if clause['footnote'] is not None:
                all_footnotes.append(clause['footnote'])
    
    all_footnotes.sort()
    print(f"Footnote range: {min(all_footnotes)} - {max(all_footnotes)}")
    print(f"Unique footnotes: {len(set(all_footnotes))}")
    
    # Find missing footnote numbers
    expected_footnotes = set(range(1, 1304))  # 1-1303
    actual_footnotes = set(all_footnotes)
    missing_footnotes = expected_footnotes - actual_footnotes
    
    print(f"Missing footnote numbers: {len(missing_footnotes)}")
    if missing_footnotes:
        print(f"Missing: {sorted(missing_footnotes)[:20]}...")
    
    # Check questions with suspiciously few clauses
    low_clause_questions = [(q['question'], len(q['clauses'])) for q in questions if len(q['clauses']) < 3]
    print(f"\nQuestions with <3 clauses: {len(low_clause_questions)}")
    for q_num, clause_count in low_clause_questions[:10]:
        print(f"  Q{q_num}: {clause_count} clauses")
    
    # Look at a specific question with few clauses
    if low_clause_questions:
        q_num = low_clause_questions[0][0]
        question = next(q for q in questions if q['question'] == q_num)
        print(f"\n=== DETAILED ANALYSIS OF Q{q_num} ===")
        print(f"Question: {question['question_text']}")
        print(f"Answer: {question['answer'][:200]}...")
        print(f"Clauses: {len(question['clauses'])}")
        for i, clause in enumerate(question['clauses']):
            print(f"  {i+1}. Footnote {clause['footnote']}: {clause['text'][:100]}...")

def check_pdf_for_missing_footnotes():
    """Check the PDF directly for missing footnote numbers"""
    doc = fitz.open(PDF_PATH)
    found_footnotes = set()
    
    # Check pages 3-41
    for page_num in range(2, 41):
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_size = span.get('size', 0)
                        
                        # Look for footnote numbers (smaller font)
                        if text.isdigit() and font_size < 9.0:
                            footnote_num = int(text)
                            if 1 <= footnote_num <= 1303:
                                found_footnotes.add(footnote_num)
    
    print(f"\n=== PDF DIRECT CHECK ===")
    print(f"Found {len(found_footnotes)} unique footnote numbers in PDF")
    print(f"Range: {min(found_footnotes)} - {max(found_footnotes)}")
    
    # Find missing in PDF
    expected_footnotes = set(range(1, 1304))
    missing_in_pdf = expected_footnotes - found_footnotes
    print(f"Missing in PDF: {len(missing_in_pdf)}")
    if missing_in_pdf:
        print(f"Missing: {sorted(missing_in_pdf)[:20]}...")

if __name__ == "__main__":
    debug_missing_clauses()
    check_pdf_for_missing_footnotes() 