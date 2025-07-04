import json
import sys

def update_catechism_with_references(catechism_file, references_file, output_file):
    """
    Update catechism file with proof texts from references file.
    
    Args:
        catechism_file: Path to catechism JSON file with footnoteNum fields
        references_file: Path to references JSON file
        output_file: Path to output updated catechism file
    """
    
    # Load the catechism file
    with open(catechism_file, 'r', encoding='utf-8') as f:
        catechism = json.load(f)
    
    # Load the references file
    with open(references_file, 'r', encoding='utf-8') as f:
        references = json.load(f)
    
    # Track statistics
    updated_clauses = 0
    missing_footnotes = []
    
    # Update each question's clauses
    for question in catechism['questions']:
        for clause in question['clauses']:
            if 'footnoteNum' in clause and clause['footnoteNum'] is not None:
                footnote_num = str(clause['footnoteNum'])
                
                if footnote_num in references:
                    clause['proofTexts'] = references[footnote_num]
                    updated_clauses += 1
                else:
                    clause['proofTexts'] = []
                    missing_footnotes.append(clause['footnoteNum'])
    
    # Write the updated catechism file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catechism, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {updated_clauses} clauses with proof texts")
    if missing_footnotes:
        print(f"Missing footnotes: {missing_footnotes}")
    else:
        print("No missing footnotes")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_catechism_with_references.py <catechism_file> <references_file> <output_file>")
        sys.exit(1)
    
    catechism_file = sys.argv[1]
    references_file = sys.argv[2]
    output_file = sys.argv[3]
    
    update_catechism_with_references(catechism_file, references_file, output_file) 