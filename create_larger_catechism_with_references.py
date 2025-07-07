#!/usr/bin/env python3
"""
Script to create a version of the Westminster Larger Catechism that includes
a 'references' array in each clause object with the corresponding references
from the references file.
"""

import json
import sys
from pathlib import Path

def load_json_file(file_path):
    """Load and return JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        sys.exit(1)

def save_json_file(data, file_path):
    """Save JSON data to a file with proper formatting."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        sys.exit(1)

def add_references_to_catechism(catechism_data, references_data):
    """
    Add references array to each clause based on footnote number.
    
    Args:
        catechism_data: List of catechism questions
        references_data: Dictionary of references keyed by footnote number
    
    Returns:
        Modified catechism data with references added
    """
    modified_catechism = []
    
    for question in catechism_data:
        modified_question = question.copy()
        modified_clauses = []
        
        for clause in question['clauses']:
            modified_clause = clause.copy()
            footnote_num = clause.get('footnote')
            
            if footnote_num is not None:
                # Convert footnote number to string to match references keys
                footnote_key = str(footnote_num)
                references = references_data.get(footnote_key, [])
                modified_clause['references'] = references
            else:
                # If no footnote, add empty references array
                modified_clause['references'] = []
            
            modified_clauses.append(modified_clause)
        
        modified_question['clauses'] = modified_clauses
        modified_catechism.append(modified_question)
    
    return modified_catechism

def main():
    """Main function to process the files."""
    # File paths
    catechism_file = Path("assets/catechisms/larger/westminster_larger_catechism_no_references.json")
    references_file = Path("assets/catechisms/larger/westminster_larger_catechism_references.json")
    output_file = Path("assets/catechisms/larger/westminster_larger_catechism_with_references.json")
    
    print("Loading catechism data...")
    catechism_data = load_json_file(catechism_file)
    
    print("Loading references data...")
    references_data = load_json_file(references_file)
    
    print("Adding references to clauses...")
    modified_catechism = add_references_to_catechism(catechism_data, references_data)
    
    print("Saving modified catechism...")
    save_json_file(modified_catechism, output_file)
    
    # Print some statistics
    total_clauses = sum(len(q['clauses']) for q in modified_catechism)
    clauses_with_references = sum(
        len([c for c in q['clauses'] if c['references']]) 
        for q in modified_catechism
    )
    
    print(f"\nProcessing complete!")
    print(f"Total questions: {len(modified_catechism)}")
    print(f"Total clauses: {total_clauses}")
    print(f"Clauses with references: {clauses_with_references}")
    print(f"Clauses without references: {total_clauses - clauses_with_references}")

if __name__ == "__main__":
    main() 