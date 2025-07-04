import json

def verify_existing_file():
    # Load the existing complete file
    with open("assets/westminster_larger_catechism_with_footnote_nums.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    
    print(f"File contains {len(questions)} questions")
    
    # Count total clauses
    total_clauses = sum(len(q['clauses']) for q in questions)
    print(f"Total clauses: {total_clauses}")
    
    # Collect all footnote numbers
    all_footnotes = []
    for q in questions:
        for clause in q['clauses']:
            if 'footnoteNum' in clause and clause['footnoteNum'] is not None:
                all_footnotes.append(clause['footnoteNum'])
    
    unique_footnotes = len(set(all_footnotes))
    print(f"Unique footnote numbers: {unique_footnotes}")
    
    # Check if we have exactly what we need
    if len(questions) == 196 and unique_footnotes == 1303:
        print("SUCCESS: File has exactly 196 questions and 1303 unique footnotes!")
        
        # Convert to the format we want
        converted_questions = []
        for q in questions:
            converted_clauses = []
            for clause in q['clauses']:
                converted_clauses.append({
                    'text': clause['text'],
                    'footnote': clause.get('footnoteNum')
                })
            
            converted_questions.append({
                'question': q['number'],
                'question_text': q['question'],
                'answer': q['answer'],
                'clauses': converted_clauses
            })
        
        # Save in our desired format
        output_data = {
            'title': 'Westminster Larger Catechism',
            'year': 1647,
            'questions': converted_questions
        }
        
        with open("assets/westminster_larger_catechism_final.json", 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print("Converted and saved to westminster_larger_catechism_final.json")
        return True
    else:
        print(f"ERROR: Expected 196 questions and 1303 footnotes, got {len(questions)} questions and {unique_footnotes} footnotes")
        return False

if __name__ == "__main__":
    verify_existing_file() 