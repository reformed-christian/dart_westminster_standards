#!/usr/bin/env python3
"""
Recreate all clauses for the Westminster Larger Catechism from scratch.
For each question, split the answer at every number, and assign that number as footnoteNum.
Ignore any existing clause data.
"""

import json
import re

def split_answer_into_clauses(answer):
    # Split at every number, keeping the number at the end of each clause
    pattern = re.compile(r'(.*?\d+)')
    return [m.group(1).strip() for m in pattern.finditer(answer)]

def recreate_clauses():
    with open('assets/westminster_larger_catechism.json', 'r') as f:
        catechism = json.load(f)

    for question in catechism['questions']:
        answer = question.get('answer', '')
        if not answer:
            question['clauses'] = []
            continue
        clauses = split_answer_into_clauses(answer)
        clause_objs = []
        for clause in clauses:
            m = re.search(r'(\d+)$', clause)
            if not m:
                continue
            footnote_num = int(m.group(1))
            clause_objs.append({
                'text': clause,
                'footnoteNum': footnote_num
            })
        question['clauses'] = clause_objs

    with open('assets/westminster_larger_catechism_fixed.json', 'w') as f:
        json.dump(catechism, f, indent=2)
    print('Recreated all clauses from scratch.')

if __name__ == '__main__':
    recreate_clauses() 