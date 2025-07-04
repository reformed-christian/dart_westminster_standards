import json
import re

INPUT_PATH = "assets/westminster_shorter_catechism_references.json"

with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    refs = json.load(f)

for footnote in refs.values():
    for entry in footnote:
        if 'reference' in entry:
            entry['reference'] = re.sub(r'\.$', '', entry['reference'].strip())

with open(INPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(refs, f, indent=2, ensure_ascii=False)

print(f"Removed trailing periods from all references in {INPUT_PATH}") 