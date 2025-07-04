import json

def update_larger_catechism_with_footnote_nums(catechism_file, references_file, output_file):
    """
    Update Larger Catechism file by adding footnoteNum fields to each clause.
    This ensures the structure matches the Shorter Catechism with footnotes.
    """
    
    # Load the catechism file
    with open(catechism_file, 'r', encoding='utf-8') as f:
        catechism = json.load(f)
    
    # Load the references file
    with open(references_file, 'r', encoding='utf-8') as f:
        references = json.load(f)
    
    # Track statistics
    updated_clauses = 0
    total_footnotes = len(references)
    
    print(f"Processing {total_footnotes} footnotes...")
    
    # First, let's see how many clauses we have total
    total_clauses = 0
    for question in catechism['questions']:
        total_clauses += len(question['clauses'])
    
    print(f"Total clauses in catechism: {total_clauses}")
    
    # If we have more footnotes than clauses, we need to create additional clauses
    if total_footnotes > total_clauses:
        print(f"Warning: {total_footnotes} footnotes but only {total_clauses} clauses")
        print("Creating additional clauses to accommodate all footnotes...")
        
        # Add additional clauses to the last question to accommodate all footnotes
        last_question = catechism['questions'][-1]
        additional_clauses_needed = total_footnotes - total_clauses
        
        for i in range(additional_clauses_needed):
            last_question['clauses'].append({
                "text": f"Additional clause {i + 1}",
                "footnoteNum": None,
                "proofTexts": []
            })
    
    # Now assign all footnotes to clauses with footnoteNum fields
    current_footnote = 1
    clause_index = 0
    
    for question in catechism['questions']:
        for clause in question['clauses']:
            if current_footnote <= total_footnotes:
                footnote_num = str(current_footnote)
                
                # Add footnoteNum field
                clause['footnoteNum'] = current_footnote
                
                if footnote_num in references:
                    clause['proofTexts'] = references[footnote_num]
                    updated_clauses += 1
                    print(f"Assigned footnote {footnote_num} to clause {clause_index + 1}")
                else:
                    clause['proofTexts'] = []
                    print(f"Warning: Footnote {footnote_num} not found in references")
                
                current_footnote += 1
            else:
                # For clauses beyond the footnotes, set footnoteNum to null
                clause['footnoteNum'] = None
            clause_index += 1
    
    # Write the updated catechism file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catechism, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessed {current_footnote - 1} footnotes")
    print(f"Updated {updated_clauses} clauses with proof texts and footnote numbers")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    catechism_file = "assets/westminster_larger_catechism.json"
    references_file = "assets/westminster_larger_catechism_references.json"
    output_file = "assets/westminster_larger_catechism_with_footnote_nums.json"
    
    update_larger_catechism_with_footnote_nums(catechism_file, references_file, output_file) 