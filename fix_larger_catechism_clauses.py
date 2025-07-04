#!/usr/bin/env python3
"""
Fix the Westminster Larger Catechism by splitting answers at every number, assigning each number as the footnoteNum for the clause ending with it.
"""

import json
import re

def split_answer_into_clauses(answer):
    # Split at every number, keeping the number at the end of each clause
    # This regex finds all text up to and including a number
    pattern = re.compile(r'(.*?\d+)')
    clauses = [m.group(1).strip() for m in pattern.finditer(answer)]
    return clauses

def fix_catechism_clauses():
    with open('assets/westminster_larger_catechism.json', 'r') as f:
        catechism = json.load(f)

    for question in catechism['questions']:
        answer = question.get('answer', '')
        if not answer:
            continue
        clauses = split_answer_into_clauses(answer)
        clause_objs = []
        for clause in clauses:
            # The footnote number is the last number in the clause
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

    print('Done.')

if __name__ == '__main__':
    fix_catechism_clauses() 