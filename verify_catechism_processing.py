#!/usr/bin/env python3
"""
Verification script to check Westminster Larger Catechism processing.
This script will:
1. Check each answer for numbers
2. Create clauses from each answer
3. Report detailed feedback on what's happening
4. Verify all requirements are met
"""

import json
import re
from typing import List, Dict, Any

def find_numbers_in_text(text: str) -> List[str]:
    """Find all numbers in text."""
    return re.findall(r'\d+', text)

def split_answer_into_clauses(answer: str) -> List[Dict[str, Any]]:
    """Split answer into clauses at every number."""
    numbers = find_numbers_in_text(answer)
    
    if not numbers:
        return []
    
    clauses = []
    current_pos = 0
    
    for i, number in enumerate(numbers):
        # Find the position of this number in the text
        number_pos = answer.find(number, current_pos)
        if number_pos == -1:
            continue
            
        # Get text up to and including this number
        clause_text = answer[current_pos:number_pos + len(number)].strip()
        if clause_text:
            clauses.append({
                "text": clause_text,
                "footnoteNum": int(number)
            })
        
        current_pos = number_pos + len(number)
    
    return clauses

def verify_catechism():
    """Main verification function."""
    with open('assets/westminster_larger_catechism.json', 'r') as f:
        catechism = json.load(f)
    
    total_questions = len(catechism['questions'])
    questions_with_numbers = 0
    questions_with_clauses = 0
    total_clauses_created = 0
    total_numbers_found = 0
    
    print(f"=== WESTMINSTER LARGER CATECHISM VERIFICATION ===\n")
    print(f"Total questions: {total_questions}\n")
    
    for i, question in enumerate(catechism['questions'], 1):
        question_num = question['number']
        answer = question.get('answer', '')
        
        # Find numbers in answer
        numbers = find_numbers_in_text(answer)
        total_numbers_found += len(numbers)
        
        # Create clauses
        clauses = split_answer_into_clauses(answer)
        total_clauses_created += len(clauses)
        
        # Status tracking
        has_numbers = len(numbers) > 0
        has_clauses = len(clauses) > 0
        
        if has_numbers:
            questions_with_numbers += 1
        if has_clauses:
            questions_with_clauses += 1
        
        # Detailed reporting for first 10 questions and any with issues
        if i <= 10 or not has_numbers or not has_clauses:
            print(f"Question {question_num}:")
            print(f"  Answer length: {len(answer)} characters")
            print(f"  Numbers found: {numbers}")
            print(f"  Clauses created: {len(clauses)}")
            
            if not has_numbers:
                print(f"  ❌ NO NUMBERS FOUND")
                print(f"  Answer preview: {answer[:100]}...")
            elif not has_clauses:
                print(f"  ❌ NUMBERS FOUND BUT NO CLAUSES CREATED")
                print(f"  Numbers: {numbers}")
            else:
                print(f"  ✅ SUCCESS: {len(clauses)} clauses created")
                for j, clause in enumerate(clauses, 1):
                    print(f"    Clause {j}: footnote {clause['footnoteNum']} - {clause['text'][:50]}...")
            
            print()
    
    # Summary statistics
    print(f"=== SUMMARY STATISTICS ===")
    print(f"Total questions: {total_questions}")
    print(f"Questions with numbers: {questions_with_numbers}")
    print(f"Questions with clauses: {questions_with_clauses}")
    print(f"Total numbers found: {total_numbers_found}")
    print(f"Total clauses created: {total_clauses_created}")
    print()
    
    # Requirements check
    print(f"=== REQUIREMENTS CHECK ===")
    if questions_with_numbers == total_questions:
        print(f"✅ All questions have numbers")
    else:
        print(f"❌ Only {questions_with_numbers}/{total_questions} questions have numbers")
    
    if questions_with_clauses == total_questions:
        print(f"✅ All questions have clauses")
    else:
        print(f"❌ Only {questions_with_clauses}/{total_questions} questions have clauses")
    
    if total_clauses_created == total_numbers_found:
        print(f"✅ All numbers converted to clauses")
    else:
        print(f"❌ Only {total_clauses_created}/{total_numbers_found} numbers converted to clauses")
    
    # Expected total clauses (should be 1303)
    print(f"Expected total clauses: 1303")
    print(f"Actual total clauses: {total_clauses_created}")
    
    if total_clauses_created == 1303:
        print(f"✅ CORRECT: All 1303 clauses created!")
    else:
        print(f"❌ INCORRECT: Expected 1303, got {total_clauses_created}")

if __name__ == "__main__":
    verify_catechism() 