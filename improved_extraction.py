import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"
OUTPUT_PATH = "assets/westminster_larger_catechism_verified.json"
HEADER_LINES = {"WESTMINSTER LARGER CATECHISM", "WITH PROOF TEXTS"}

# Feedback loop: verify cleansing does not remove valid content or footnotes
def cleanse_and_verify(all_lines):
    # Before cleansing: collect all footnote-like numbers in context
    footnote_regex = re.compile(r"\b(\d{1,4})\b")
    before_footnotes = set()
    for line in all_lines:
        for m in footnote_regex.finditer(line):
            before_footnotes.add(int(m.group(1)))
    before_len = len(all_lines)
    
    # Cleansing: remove only true page numbers and known headers
    cleansed = []
    removed = []
    for line in all_lines:
        if not line or (line.isdigit() and len(line) < 4):
            removed.append(line)
            continue
        if line in HEADER_LINES:
            removed.append(line)
            continue
        cleansed.append(line)
    after_footnotes = set()
    for line in cleansed:
        for m in footnote_regex.finditer(line):
            after_footnotes.add(int(m.group(1)))
    after_len = len(cleansed)
    # Feedback diagnostics
    print(f"Cleansing: {before_len} lines -> {after_len} lines")
    lost_footnotes = before_footnotes - after_footnotes
    if lost_footnotes:
        print(f"❌ WARNING: Lost footnote-like numbers: {sorted(lost_footnotes)[:10]} ...")
        print(f"Removed lines containing lost footnotes:")
        for line in removed:
            for num in lost_footnotes:
                if str(num) in line:
                    print(f"  {line}")
    else:
        print("✅ No valid footnote numbers lost in cleansing.")
    return cleansed

# Step 1: Extract all text from pages 3-41 (zero-based 2-40) with page tracking
def extract_all_text_with_pages():
    doc = fitz.open(PDF_PATH)
    all_lines = []
    for page_num in range(2, 41):
        page = doc[page_num]
        text = page.get_text()
        for line in text.splitlines():
            line = line.strip()
            if line:  # Keep all non-empty lines for now
                all_lines.append((line, page_num))
    return all_lines

# Step 2: Identify all question headers and split into Q/A pairs with page tracking
def split_questions_answers_with_pages(all_lines_with_pages):
    qa_pairs = []
    current_q = None
    current_a = []
    current_pages = set()
    question_pattern = re.compile(r'^Q\.\s*(\d+)\.\s*(.*)$')
    
    for line, page_num in all_lines_with_pages:
        match = question_pattern.match(line)
        if match:
            if current_q is not None:
                qa_pairs.append((current_q, current_a, current_pages))
            current_q = {'number': int(match.group(1)), 'text': match.group(2)}
            current_a = []
            current_pages = {page_num}
        else:
            if current_q is not None:
                current_a.append(line)
                current_pages.add(page_num)
    
    if current_q is not None:
        qa_pairs.append((current_q, current_a, current_pages))
    return qa_pairs

# Step 3: Verify no answer chunks are lost at page boundaries
def verify_page_boundaries(qa_pairs):
    print("\nVerifying page boundary continuity...")
    suspicious_answers = []
    
    for q, a, pages in qa_pairs:
        if len(pages) > 1:  # Multi-page answers
            answer_text = ' '.join(a)
            # Only flag answers that are suspiciously short (likely truncated)
            if len(answer_text) < 30:  # Very short answers might be truncated
                suspicious_answers.append((q['number'], answer_text, pages))
            # Check for obvious truncation patterns (incomplete words, etc.)
            if answer_text.endswith('...') or answer_text.endswith('..'):
                suspicious_answers.append((q['number'], answer_text, pages))
    
    if suspicious_answers:
        print(f"❌ WARNING: {len(suspicious_answers)} potentially truncated answers:")
        for q_num, text, pages in suspicious_answers[:5]:
            print(f"  Q{q_num} (pages {sorted(pages)}): {text[:100]}...")
        if len(suspicious_answers) > 5:
            print("  ...")
        return False
    else:
        print("✅ No suspicious page boundary breaks detected.")
        return True

def verify_and_report(qa_pairs, all_lines):
    print(f"Total Q/A pairs: {len(qa_pairs)}")
    if len(qa_pairs) != 196:
        print(f"❌ ERROR: Expected 196 questions, found {len(qa_pairs)}")
        for i, (q, a, _) in enumerate(qa_pairs):
            print(f"Q{i+1}: {q['number']} ({len(a)} answer lines)")
        return False
    
    # Convert back to simple format for existing verification
    simple_qa_pairs = [(q, a) for q, a, _ in qa_pairs]
    all_lines_simple = [line for line, _ in all_lines]
    
    assigned_lines = set()
    for q, a in simple_qa_pairs:
        assigned_lines.add(f"Q. {q['number']}. {q['text']}")
        assigned_lines.update(a)
    leftovers = [line for line in all_lines_simple if line not in assigned_lines]
    if leftovers:
        print(f"❌ ERROR: {len(leftovers)} unassigned lines:")
        for line in leftovers[:10]:
            print(f"  {line}")
        if len(leftovers) > 10:
            print("  ...")
        return False
    print("✅ All text accounted for. 196 questions and answers extracted.")
    return True

def main():
    print(f"Extracting all text from {PDF_PATH} (pages 3-41)...")
    all_lines_with_pages = extract_all_text_with_pages()
    print(f"Total lines extracted: {len(all_lines_with_pages)}")
    
    # Cleanse with verification
    all_lines_simple = [line for line, _ in all_lines_with_pages]
    cleansed_lines_simple = cleanse_and_verify(all_lines_simple)
    
    # Reconstruct with page tracking for cleansed lines
    cleansed_lines_with_pages = []
    cleansed_set = set(cleansed_lines_simple)
    for line, page in all_lines_with_pages:
        if line in cleansed_set:
            cleansed_lines_with_pages.append((line, page))
    
    qa_pairs = split_questions_answers_with_pages(cleansed_lines_with_pages)
    
    # Verify page boundaries
    page_ok = verify_page_boundaries(qa_pairs)
    
    # Standard verification
    ok = verify_and_report(qa_pairs, cleansed_lines_with_pages)
    
    if not ok or not page_ok:
        print("Extraction failed verification. Please review diagnostics above.")
        return
    
    # Save output
    output = []
    for q, a, _ in qa_pairs:
        output.append({
            'question': q['number'],
            'question_text': q['text'],
            'answer': ' '.join(a)
        })
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Output written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 