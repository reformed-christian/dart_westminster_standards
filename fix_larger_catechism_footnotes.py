import json

def fix_larger_catechism_footnotes(catechism_file, references_file, output_file):
    """
    Fix the Larger Catechism by properly assigning footnotes to clauses.
    This script does NOT create fake "Additional clause" entries.
    Instead, it assigns footnotes to their proper locations and leaves
    clauses without footnotes as null.
    """
    
    # Load the catechism file
    with open(catechism_file, 'r', encoding='utf-8') as f:
        catechism = json.load(f)
    
    # Load the references file
    with open(references_file, 'r', encoding='utf-8') as f:
        references = json.load(f)
    
    # Track statistics
    total_clauses = 0
    clauses_with_footnotes = 0
    
    print(f"Processing {len(references)} footnotes...")
    
    # Count total clauses first
    for question in catechism['questions']:
        total_clauses += len(question['clauses'])
    
    print(f"Total clauses in catechism: {total_clauses}")
    print(f"Total footnotes available: {len(references)}")
    
    # Process each question and clause
    clause_index = 0
    
    for question in catechism['questions']:
        for clause in question['clauses']:
            clause_index += 1
            
            # Check if this clause should have a footnote
            footnote_num = str(clause_index)
            
            if footnote_num in references:
                # This clause gets a footnote
                clause['footnoteNum'] = clause_index
                clause['proofTexts'] = references[footnote_num]
                clauses_with_footnotes += 1
                print(f"Assigned footnote {footnote_num} to clause {clause_index}")
            else:
                # This clause doesn't have a footnote - that's fine
                clause['footnoteNum'] = None
                # Keep existing proofTexts if any, otherwise empty array
                if 'proofTexts' not in clause:
                    clause['proofTexts'] = []
    
    # Write the updated catechism file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catechism, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessed {total_clauses} total clauses")
    print(f"Assigned footnotes to {clauses_with_footnotes} clauses")
    print(f"Left {total_clauses - clauses_with_footnotes} clauses without footnotes (as expected)")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    catechism_file = "assets/westminster_larger_catechism.json"
    references_file = "assets/westminster_larger_catechism_references.json"
    output_file = "assets/westminster_larger_catechism_fixed.json"
    
    fix_larger_catechism_footnotes(catechism_file, references_file, output_file) 