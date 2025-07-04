import json
import re

INPUT_PATH = "assets/westminster_larger_catechism_span_extracted.json"
OUTPUT_PATH = "assets/westminster_larger_catechism_clauses.json"
FOOTNOTE_RANGE = range(1, 1304)  # 1 to 1303 inclusive

def verify_input_data(data):
    """Verify input data integrity"""
    print("Step 1: Verifying input data...")
    
    if len(data) != 196:
        print(f"❌ ERROR: Expected 196 questions, found {len(data)}")
        return False
    
    # Check that each answer contains footnote numbers
    footnote_regex = re.compile(r"\b(\d{1,4})\b")
    total_footnotes_in_answers = set()
    
    for q in data:
        answer = q["answer"]
        footnotes = [int(m.group(1)) for m in footnote_regex.finditer(answer)]
        valid_footnotes = [f for f in footnotes if f in FOOTNOTE_RANGE]
        total_footnotes_in_answers.update(valid_footnotes)
    
    print(f"  Found {len(total_footnotes_in_answers)} unique footnote numbers in answers")
    print(f"  Footnote range: {min(total_footnotes_in_answers)} - {max(total_footnotes_in_answers)}")
    
    if len(total_footnotes_in_answers) != 1303:
        print(f"❌ ERROR: Expected 1303 footnotes, found {len(total_footnotes_in_answers)}")
        missing = set(FOOTNOTE_RANGE) - total_footnotes_in_answers
        print(f"  Missing footnotes: {sorted(missing)[:10]}...")
        return False
    
    print("✅ Input data verified successfully")
    return True

def split_answer_into_clauses(answer):
    """
    Splits answer into clauses at footnote numbers.
    Excludes list numbering (numbers followed by periods like "1.", "2.").
    Returns a list of dicts: {"text": ..., "footnote": ...}
    """
    clauses = []
    # Look for numbers that are NOT followed by a period (actual footnotes)
    footnote_regex = re.compile(r"\b(\d{1,4})\b(?!\.)")
    
    # Find all footnote positions
    footnote_positions = []
    for match in footnote_regex.finditer(answer):
        num = int(match.group(1))
        if num in FOOTNOTE_RANGE:
            footnote_positions.append((match.start(), match.end(), num))
    
    if not footnote_positions:
        # No footnotes found - create one clause with entire answer
        return [{"text": answer.strip(), "footnote": None}]
    
    # Create clauses for valid footnotes
    for i, (start, end, footnote_num) in enumerate(footnote_positions):
        if i > 0:
            prev_end = footnote_positions[i-1][1]
            clause_text = answer[prev_end:start].strip()
        else:
            clause_text = answer[:start].strip()
        
        # Include the footnote number in the clause text
        clause_text += " " + str(footnote_num)
        
        clauses.append({
            "text": clause_text,
            "footnote": footnote_num
        })
    
    # Handle trailing text
    if footnote_positions:
        last_end = footnote_positions[-1][1]
        trailing_text = answer[last_end:].strip()
        if trailing_text:
            clauses[-1]["text"] += " " + trailing_text
    
    return clauses

def verify_clause_extraction(all_clauses):
    """Verify clause extraction integrity"""
    print("\nStep 2: Verifying clause extraction...")
    
    # Count verification
    total_clauses = sum(len(q["clauses"]) for q in all_clauses)
    print(f"  Total clauses extracted: {total_clauses}")
    
    # Count answers without footnotes
    answers_without_footnotes = 0
    for q in all_clauses:
        if len(q["clauses"]) == 1 and q["clauses"][0]["footnote"] is None:
            answers_without_footnotes += 1
    
    print(f"  Answers without footnotes: {answers_without_footnotes}")
    print(f"  Expected clauses: 1303 + {answers_without_footnotes} = {1303 + answers_without_footnotes}")
    
    expected_clauses = 1303 + answers_without_footnotes
    if total_clauses != expected_clauses:
        print(f"❌ ERROR: Expected {expected_clauses} clauses, found {total_clauses}")
        return False
    
    # Footnote coverage verification
    all_footnotes = set()
    duplicate_footnotes = []
    orphan_clauses = []
    
    for q in all_clauses:
        for clause in q["clauses"]:
            if clause["footnote"] is None:
                # This is an answer without footnotes - skip verification
                continue
            if clause["footnote"] in all_footnotes:
                duplicate_footnotes.append(clause["footnote"])
            all_footnotes.add(clause["footnote"])
    
    print(f"  Unique footnotes: {len(all_footnotes)}")
    
    # Check for missing footnotes
    missing_footnotes = set(FOOTNOTE_RANGE) - all_footnotes
    if missing_footnotes:
        print(f"❌ ERROR: Missing footnotes: {sorted(missing_footnotes)[:10]}...")
        return False
    
    # Check for duplicate footnotes
    if duplicate_footnotes:
        print(f"❌ ERROR: Duplicate footnotes: {duplicate_footnotes[:10]}...")
        return False
    
    print("✅ Clause extraction verified successfully")
    return True

def verify_text_preservation(original_data, all_clauses):
    """Verify no text is lost during clause extraction"""
    print("\nStep 3: Verifying text preservation...")
    
    for i, (original_q, clause_q) in enumerate(zip(original_data, all_clauses)):
        original_text = original_q["answer"]
        clause_text = " ".join(clause["text"] for clause in clause_q["clauses"])
        
        # Normalize whitespace for comparison
        original_normalized = re.sub(r'\s+', ' ', original_text).strip()
        clause_normalized = re.sub(r'\s+', ' ', clause_text).strip()
        
        if original_normalized != clause_normalized:
            print(f"❌ ERROR: Text mismatch in Q{original_q['question']}")
            print(f"  Original: {original_normalized[:100]}...")
            print(f"  Clauses:  {clause_normalized[:100]}...")
            return False
    
    print("✅ Text preservation verified successfully")
    return True

def main():
    print("Extracting clauses from verified Q/A data...")
    
    # Load input data
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Step 1: Verify input data
    if not verify_input_data(data):
        print("❌ Input verification failed. Stopping.")
        return
    
    # Step 2: Extract clauses
    print("\nExtracting clauses...")
    all_clauses = []
    for q in data:
        clauses = split_answer_into_clauses(q["answer"])
        all_clauses.append({
            "question": q["question"],
            "question_text": q["question_text"],
            "clauses": clauses
        })
    
    # Step 3: Verify clause extraction
    if not verify_clause_extraction(all_clauses):
        print("❌ Clause extraction verification failed. Stopping.")
        return
    
    # Step 4: Verify text preservation
    if not verify_text_preservation(data, all_clauses):
        print("❌ Text preservation verification failed. Stopping.")
        return
    
    # All verifications passed - save output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_clauses, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ All verifications passed!")
    print(f"Output written to: {OUTPUT_PATH}")
    print(f"Summary: 196 questions, 1303 clauses, all footnotes accounted for")

if __name__ == "__main__":
    main() 