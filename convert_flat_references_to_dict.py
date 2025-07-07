#!/usr/bin/env python3
import json
from collections import defaultdict

input_file = "westminster_shorter_catechism_references_font_based.json"
output_file = "westminster_shorter_catechism_references_font_based_dict_from_flat.json"

def main():
    with open(input_file, 'r', encoding='utf-8') as f:
        refs = json.load(f)
    
    grouped = defaultdict(list)
    for ref in refs:
        key = str(ref["footnote_number"])
        grouped[key].append({
            "reference": ref["reference"],
            "text": ref["scripture_text"]
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(grouped, f, indent=2, ensure_ascii=False)
    print(f"Converted {len(refs)} references into {len(grouped)} footnotes. Output: {output_file}")

if __name__ == "__main__":
    main() 