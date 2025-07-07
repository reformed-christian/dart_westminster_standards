#!/usr/bin/env python3
"""
Diagnostic script for Westminster Shorter Catechism extraction
Analyzes the current extraction and identifies issues that need fixing
"""

import json
import re
from collections import defaultdict

def load_shorter_catechism():
    """Load the current Shorter Catechism data"""
    with open('assets/catechisms/shorter/westminster_shorter_catechism.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_questions(data):
    """Analyze the questions structure"""
    questions = data['questions']
    print(f"\n=== QUESTIONS ANALYSIS ===")
    print(f"Total questions: {len(questions)}")
    
    # Check question numbering
    expected_numbers = list(range(1, len(questions) + 1))
    actual_numbers = [q['number'] for q in questions]
    
    if actual_numbers == expected_numbers:
        print("✓ Question numbering is sequential and correct")
    else:
        print("✗ Question numbering issues:")
        print(f"  Expected: {expected_numbers}")
        print(f"  Actual: {actual_numbers}")
    
    # Check for missing or malformed questions
    for i, q in enumerate(questions):
        if not q.get('question') or not q.get('answer'):
            print(f"✗ Question {q.get('number', i+1)} missing question or answer text")
        
        if not q.get('clauses'):
            print(f"✗ Question {q.get('number', i+1)} missing clauses")

def analyze_clauses(data):
    """Analyze the clauses structure"""
    questions = data['questions']
    print(f"\n=== CLAUSES ANALYSIS ===")
    
    total_clauses = 0
    clauses_with_footnotes = 0
    clauses_without_footnotes = 0
    
    for q in questions:
        clauses = q.get('clauses', [])
        total_clauses += len(clauses)
        
        for clause in clauses:
            if clause.get('footnoteNum'):
                clauses_with_footnotes += 1
            else:
                clauses_without_footnotes += 1
    
    print(f"Total clauses: {total_clauses}")
    print(f"Clauses with footnotes: {clauses_with_footnotes}")
    print(f"Clauses without footnotes: {clauses_without_footnotes}")
    
    # Check for text issues in clauses
    print(f"\n=== CLAUSE TEXT ISSUES ===")
    for q in questions:
        for i, clause in enumerate(q.get('clauses', [])):
            text = clause.get('text', '')
            
            # Check for common issues
            if text.startswith(')'):
                print(f"✗ Question {q['number']}, clause {i+1}: Starts with closing parenthesis")
            
            if text.endswith(','):
                print(f"⚠ Question {q['number']}, clause {i+1}: Ends with comma")
            
            if not text.strip():
                print(f"✗ Question {q['number']}, clause {i+1}: Empty text")

def analyze_footnotes(data):
    """Analyze the footnotes structure"""
    print(f"\n=== FOOTNOTES ANALYSIS ===")
    
    # Count footnotes in questions
    question_footnotes = set()
    for q in data['questions']:
        for clause in q.get('clauses', []):
            if clause.get('footnoteNum'):
                question_footnotes.add(clause['footnoteNum'])
    
    # Count footnotes in footnotes section
    footnote_section = data.get('footnotes', [])
    footnote_section_numbers = {f.get('footnote_num') for f in footnote_section}
    
    print(f"Footnotes referenced in questions: {len(question_footnotes)}")
    print(f"Footnotes in footnotes section: {len(footnote_section_numbers)}")
    
    # Check for mismatches
    missing_in_section = question_footnotes - footnote_section_numbers
    extra_in_section = footnote_section_numbers - question_footnotes
    
    if missing_in_section:
        print(f"✗ Footnotes missing from section: {sorted(missing_in_section)}")
    
    if extra_in_section:
        print(f"⚠ Extra footnotes in section: {sorted(extra_in_section)}")
    
    if not missing_in_section and not extra_in_section:
        print("✓ All footnotes properly matched")

def analyze_answer_text(data):
    """Analyze the answer text structure"""
    print(f"\n=== ANSWER TEXT ANALYSIS ===")
    
    for q in data['questions']:
        answer = q.get('answer', '')
        clauses = q.get('clauses', [])
        
        # Reconstruct answer from clauses
        reconstructed = ''
        for clause in clauses:
            text = clause.get('text', '')
            reconstructed += text
        
        # Compare with original answer
        if reconstructed.strip() != answer.strip():
            print(f"✗ Question {q['number']}: Answer text mismatch")
            print(f"  Original: {answer}")
            print(f"  Reconstructed: {reconstructed}")
            print()

def analyze_proof_texts(data):
    """Analyze proof texts in clauses"""
    print(f"\n=== PROOF TEXTS ANALYSIS ===")
    
    total_proof_texts = 0
    clauses_with_proof_texts = 0
    
    for q in data['questions']:
        for clause in q.get('clauses', []):
            proof_texts = clause.get('proofTexts', [])
            if proof_texts:
                clauses_with_proof_texts += 1
                total_proof_texts += len(proof_texts)
    
    print(f"Total proof texts: {total_proof_texts}")
    print(f"Clauses with proof texts: {clauses_with_proof_texts}")
    
    # Check for proof text structure issues
    for q in data['questions']:
        for i, clause in enumerate(q.get('clauses', [])):
            proof_texts = clause.get('proofTexts', [])
            for j, pt in enumerate(proof_texts):
                if not pt.get('reference') or not pt.get('text'):
                    print(f"✗ Question {q['number']}, clause {i+1}, proof text {j+1}: Missing reference or text")

def check_for_common_issues(data):
    """Check for common extraction issues"""
    print(f"\n=== COMMON ISSUES CHECK ===")
    
    # Check for list numbering in footnotes
    for q in data['questions']:
        for clause in q.get('clauses', []):
            text = clause.get('text', '')
            if re.search(r'\b\d+\.\s', text):
                print(f"⚠ Question {q['number']}: Possible list numbering in text: {text[:100]}...")
    
    # Check for missing answer indicators
    for q in data['questions']:
        answer = q.get('answer', '')
        if answer.startswith('A. '):
            print(f"⚠ Question {q['number']}: Answer still has 'A. ' prefix")
    
    # Check for footnote numbers in text
    for q in data['questions']:
        answer = q.get('answer', '')
        if re.search(r'\b\d+\b', answer):
            print(f"⚠ Question {q['number']}: Possible footnote numbers in answer text")

def main():
    """Main diagnostic function"""
    print("Westminster Shorter Catechism Diagnostic")
    print("=" * 50)
    
    try:
        data = load_shorter_catechism()
        
        analyze_questions(data)
        analyze_clauses(data)
        analyze_footnotes(data)
        analyze_answer_text(data)
        analyze_proof_texts(data)
        check_for_common_issues(data)
        
        print(f"\n=== SUMMARY ===")
        print(f"Total questions: {len(data['questions'])}")
        print(f"Total clauses: {sum(len(q.get('clauses', [])) for q in data['questions'])}")
        print(f"Total footnotes: {len(data.get('footnotes', []))}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 