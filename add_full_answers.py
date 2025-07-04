import json

def add_full_answers():
    """Add full cleaned answer text by combining all clauses for each question, and rename properties."""
    
    # Load the data
    with open("assets/westminster_larger_catechism.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("Adding full answer text and renaming properties...")
    
    new_data = []
    for q in data:
        clauses = q["clauses"]
        
        # Combine all clause texts to create the full answer
        full_answer_parts = []
        for clause in clauses:
            text = clause["text"].strip()
            if text:
                full_answer_parts.append(text)
        full_answer = " ".join(full_answer_parts)
        full_answer = " ".join(full_answer.split())
        
        # Build new question object with renamed properties
        new_q = {
            "number": q["question"],
            "question": q["question_text"],
            "clauses": clauses,
            "answer": full_answer
        }
        new_data.append(new_q)
        
        # Print a sample for verification
        if new_q["number"] <= 3:
            print(f"Q{new_q['number']}: {new_q['question']}")
            print(f"  Answer: {new_q['answer'][:100]}...")
            print()
    
    # Save the enhanced data
    output_path = "assets/westminster_larger_catechism_final.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Final data saved to: {output_path}")
    
    # Verify the enhancement
    print("\nVerifying final data...")
    verification_passed = True
    for q in new_data:
        if "number" not in q or "question" not in q or "answer" not in q:
            print(f"❌ ERROR: Q{q.get('number', '?')} missing required fields")
            verification_passed = False
        elif not q["answer"].strip():
            print(f"❌ ERROR: Q{q['number']} has empty answer")
            verification_passed = False
    if verification_passed:
        print("✅ All questions have correct fields and answer text!")
        total_chars = sum(len(q["answer"]) for q in new_data)
        avg_length = total_chars / len(new_data)
        print(f"Total characters in all answers: {total_chars:,}")
        print(f"Average answer length: {avg_length:.1f} characters")
    else:
        print("❌ Some issues found - please check the output above")

if __name__ == "__main__":
    add_full_answers() 