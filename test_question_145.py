import json

def test_question_145():
    # Load the final file
    with open("assets/westminster_larger_catechism_final.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find question 145
    q145 = None
    for q in data['questions']:
        if q['question'] == 145:
            q145 = q
            break
    
    if not q145:
        print("ERROR: Question 145 not found!")
        return
    
    print(f"=== QUESTION 145 ===")
    print(f"Question: {q145['question_text']}")
    print(f"Answer length: {len(q145['answer'])} characters")
    print(f"Number of clauses: {len(q145['clauses'])}")
    
    # Extract all footnote numbers
    footnotes = []
    for clause in q145['clauses']:
        if clause['footnote'] is not None:
            footnotes.append(clause['footnote'])
    
    footnotes.sort()
    print(f"\nFootnote numbers: {footnotes}")
    print(f"Footnote range: {min(footnotes)} - {max(footnotes)}")
    print(f"Total footnotes: {len(footnotes)}")
    
    # Check if we have the expected range 864-909
    expected_range = set(range(864, 910))  # 864 to 909 inclusive
    actual_footnotes = set(footnotes)
    
    if actual_footnotes == expected_range:
        print("✅ SUCCESS: Question 145 contains exactly footnotes 864-909!")
    else:
        missing = expected_range - actual_footnotes
        extra = actual_footnotes - expected_range
        print(f"❌ ERROR: Mismatch in footnote numbers")
        if missing:
            print(f"Missing footnotes: {sorted(missing)}")
        if extra:
            print(f"Extra footnotes: {sorted(extra)}")
    
    # Show first few clauses
    print(f"\nFirst 5 clauses:")
    for i, clause in enumerate(q145['clauses'][:5]):
        print(f"  {i+1}. Footnote {clause['footnote']}: {clause['text'][:80]}...")
    
    # Show last few clauses
    print(f"\nLast 5 clauses:")
    for i, clause in enumerate(q145['clauses'][-5:]):
        print(f"  {len(q145['clauses']) - 4 + i}. Footnote {clause['footnote']}: {clause['text'][:80]}...")

if __name__ == "__main__":
    test_question_145() 