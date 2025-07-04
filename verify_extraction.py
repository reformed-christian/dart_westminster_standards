import json

def verify_extraction():
    # Load the corrected extraction
    with open("assets/westminster_larger_catechism_corrected.json", 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Total questions: {len(questions)}")
    print(f"Total clauses: {sum(len(q['clauses']) for q in questions)}")
    
    # Check questions with zero clauses
    zero_clause_questions = [q for q in questions if len(q['clauses']) == 0]
    if zero_clause_questions:
        print(f"\nQuestions with zero clauses: {[q['question'] for q in zero_clause_questions]}")
    else:
        print("\nAll questions have at least one clause!")
    
    # Check questions with many clauses
    many_clause_questions = [q for q in questions if len(q['clauses']) > 20]
    print(f"\nQuestions with >20 clauses: {len(many_clause_questions)}")
    for q in many_clause_questions[:5]:
        print(f"  Q{q['question']}: {len(q['clauses'])} clauses")
    
    # Look at a specific question to verify quality
    sample_question = questions[0]  # Q1
    print(f"\n=== SAMPLE: Q{sample_question['question']} ===")
    print(f"Question: {sample_question['question_text']}")
    print(f"Answer length: {len(sample_question['answer'])} characters")
    print(f"Number of clauses: {len(sample_question['clauses'])}")
    
    print("\nFirst 3 clauses:")
    for i, clause in enumerate(sample_question['clauses'][:3]):
        print(f"  {i+1}. Footnote {clause['footnote']}: {clause['text'][:80]}...")
    
    # Check footnote number distribution
    all_footnotes = []
    for q in questions:
        for clause in q['clauses']:
            if clause['footnote'] is not None:
                all_footnotes.append(clause['footnote'])
    
    all_footnotes.sort()
    print(f"\nFootnote number range: {min(all_footnotes)} - {max(all_footnotes)}")
    print(f"Unique footnote numbers: {len(set(all_footnotes))}")
    
    # Check for gaps in footnote numbers
    expected_footnotes = set(range(1, max(all_footnotes) + 1))
    actual_footnotes = set(all_footnotes)
    missing_footnotes = expected_footnotes - actual_footnotes
    if missing_footnotes:
        print(f"Missing footnote numbers: {sorted(missing_footnotes)[:10]}...")
    else:
        print("No missing footnote numbers!")

if __name__ == "__main__":
    verify_extraction() 