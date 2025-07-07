#!/usr/bin/env python3
"""
Script to reorder properties in the Westminster Larger Catechism no_references JSON file
so that 'answer' comes before 'clauses'.
"""

import json
import sys

def reorder_catechism_properties(input_file, output_file):
    """Reorder properties so 'answer' comes before 'clauses'."""
    
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Reorder properties for each catechism item
    reordered_data = []
    for item in data:
        # Create new item with desired property order
        reordered_item = {
            'number': item['number'],
            'question': item['question'],
            'answer': item['answer'],
            'clauses': item['clauses']
        }
        reordered_data.append(reordered_item)
    
    # Write the reordered data back to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(reordered_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully reordered properties in {output_file}")
    print(f"New property order: number, question, answer, clauses")

if __name__ == "__main__":
    input_file = "assets/catechisms/larger/westminster_larger_catechism_no_references.json"
    output_file = "assets/catechisms/larger/westminster_larger_catechism_no_references.json"
    
    try:
        reorder_catechism_properties(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 