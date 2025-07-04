import json

def check_original_source():
    # Load the original source file
    with open("assets/westminster_larger_catechism_with_footnote_nums.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find question 145
    q145 = None
    for q in data['questions']:
        if q['number'] == 145:
            q145 = q
            break
    
    if not q145:
        print("ERROR: Question 145 not found in original source!")
        return
    
    print(f"=== ORIGINAL SOURCE - QUESTION 145 ===")
    print(f"Question: {q145['question']}")
    print(f"Answer: {q145['answer'][:200]}...")
    print(f"Number of clauses: {len(q145['clauses'])}")
    
    # Extract all footnote numbers
    footnotes = []
    for clause in q145['clauses']:
        if 'footnoteNum' in clause and clause['footnoteNum'] is not None:
            footnotes.append(clause['footnoteNum'])
    
    footnotes.sort()
    print(f"\nFootnote numbers: {footnotes}")
    print(f"Footnote range: {min(footnotes)} - {max(footnotes)}")
    print(f"Total footnotes: {len(footnotes)}")
    
    # Check if this matches what we expect (864-909)
    expected_range = set(range(864, 910))
    actual_footnotes = set(footnotes)
    
    if actual_footnotes == expected_range:
        print("✅ SUCCESS: Original source has correct footnotes 864-909!")
    else:
        missing = expected_range - actual_footnotes
        extra = actual_footnotes - expected_range
        print(f"❌ ERROR: Original source has incorrect footnote numbers")
        if missing:
            print(f"Missing footnotes: {sorted(missing)}")
        if extra:
            print(f"Extra footnotes: {sorted(extra)}")
    
    # Show first few clauses
    print(f"\nFirst 5 clauses:")
    for i, clause in enumerate(q145['clauses'][:5]):
        print(f"  {i+1}. Footnote {clause.get('footnoteNum')}: {clause['text'][:80]}...")

if __name__ == "__main__":
    check_original_source() 