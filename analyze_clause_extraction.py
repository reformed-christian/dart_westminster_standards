import json

def analyze_clause_extraction():
    # Load the extracted data
    with open("assets/westminster_larger_catechism_extracted.json", 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Total questions: {len(questions)}")
    print(f"Total clauses: {sum(len(q['clauses']) for q in questions)}")
    
    # Analyze questions with many clauses
    questions_with_many_clauses = [(q['question'], len(q['clauses'])) for q in questions if len(q['clauses']) > 20]
    questions_with_many_clauses.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nQuestions with >20 clauses:")
    for q_num, clause_count in questions_with_many_clauses[:10]:
        print(f"  Q{q_num}: {clause_count} clauses")
    
    # Look at a specific question with many clauses
    if questions_with_many_clauses:
        q_num = questions_with_many_clauses[0][0]
        question = next(q for q in questions if q['question'] == q_num)
        
        print(f"\n=== DETAILED ANALYSIS OF Q{q_num} ===")
        print(f"Question text: {question['question_text']}")
        print(f"Answer length: {len(question['answer'])} characters")
        print(f"Number of clauses: {len(question['clauses'])}")
        
        print("\nFirst 10 clauses:")
        for i, clause in enumerate(question['clauses'][:10]):
            print(f"  {i+1}. Footnote {clause['footnote']}: {clause['text'][:100]}...")
        
        # Check for suspicious footnote numbers
        footnotes = [c['footnote'] for c in question['clauses'] if c['footnote'] is not None]
        footnotes.sort()
        print(f"\nFootnote numbers: {footnotes[:20]}...")
        
        # Check for duplicate footnotes
        from collections import Counter
        footnote_counts = Counter(footnotes)
        duplicates = {k: v for k, v in footnote_counts.items() if v > 1}
        if duplicates:
            print(f"Duplicate footnotes: {duplicates}")

if __name__ == "__main__":
    analyze_clause_extraction() 