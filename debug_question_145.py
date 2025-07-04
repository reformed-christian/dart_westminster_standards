import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"

def debug_question_145():
    doc = fitz.open(PDF_PATH)
    
    # Find which pages contain Q145
    q145_pages = []
    
    for page_num in range(2, 41):  # pages 3-41
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    line_text = ""
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_size = span.get('size', 0)
                        
                        # Skip page numbers
                        if text.isdigit() and font_size >= 9.5:
                            continue
                        
                        line_text += text + " "
                    
                    line_text = line_text.strip()
                    if not line_text:
                        continue
                    
                    # Check if this line contains Q145
                    if "Q. 145." in line_text or "Q.145." in line_text:
                        q145_pages.append(page_num + 1)  # Convert to 1-based
                        print(f"Found Q145 on page {page_num + 1}: {line_text[:100]}...")
    
    print(f"Q145 appears on pages: {q145_pages}")
    
    # Now extract Q145 with its complete content
    if len(q145_pages) >= 2:
        start_page = q145_pages[0] - 1  # Convert back to 0-based
        end_page = q145_pages[-1] - 1
        
        print(f"\nExtracting Q145 from pages {start_page + 1} to {end_page + 1}")
        
        # Extract all spans for Q145
        all_spans = []
        found_question = False
        
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num]
            text_dict = page.get_text("dict")
            
            print(f"\n=== PAGE {page_num + 1} ===")
            
            for block in text_dict.get('blocks', []):
                if block.get('type') == 0:
                    for line in block.get('lines', []):
                        line_text = ""
                        line_spans = []
                        
                        for span in line.get('spans', []):
                            text = span.get('text', '').strip()
                            font_size = span.get('size', 0)
                            font_name = span.get('font', '')
                            
                            # Skip page numbers
                            if text.isdigit() and font_size >= 9.5:
                                continue
                            
                            line_spans.append({
                                'text': text,
                                'font_size': font_size,
                                'font_name': font_name
                            })
                            line_text += text + " "
                        
                        line_text = line_text.strip()
                        if not line_text:
                            continue
                        
                        # Check if we found Q145
                        if "Q. 145." in line_text or "Q.145." in line_text:
                            found_question = True
                            print(f"FOUND Q145: {line_text}")
                            continue
                        
                        # If we found Q145, collect answer spans
                        if found_question:
                            # Check if we hit the next question
                            if re.match(r'^Q\.\s*\d+\.', line_text):
                                print(f"NEXT QUESTION FOUND: {line_text}")
                                break
                            
                            print(f"ANSWER LINE: {line_text}")
                            all_spans.extend(line_spans)
        
        # Extract clauses from spans
        clauses = extract_clauses_from_spans(all_spans)
        
        print(f"\n=== Q145 ANALYSIS ===")
        print(f"Total spans collected: {len(all_spans)}")
        print(f"Clauses extracted: {len(clauses)}")
        
        # Show footnote numbers found
        footnotes = [c['footnote'] for c in clauses if c['footnote'] is not None]
        print(f"Footnote numbers: {footnotes}")
        
        # Show first few clauses
        for i, clause in enumerate(clauses[:5]):
            print(f"  {i+1}. Footnote {clause['footnote']}: {clause['text'][:80]}...")

def extract_clauses_from_spans(spans):
    """Extract clauses from spans, splitting at footnote numbers"""
    clauses = []
    current_clause = ""
    current_footnote = None
    
    for span in spans:
        text = span['text']
        font_size = span['font_size']
        
        # Check if this is a footnote number (smaller font, 8.4pt)
        if text.isdigit() and font_size < 9.0:
            # Save previous clause if exists
            if current_clause.strip():
                clauses.append({
                    'text': current_clause.strip(),
                    'footnote': current_footnote
                })
            
            # Start new clause
            current_footnote = int(text)
            current_clause = ""
        else:
            # Add to current clause
            current_clause += " " + text
    
    # Save last clause
    if current_clause.strip():
        clauses.append({
            'text': current_clause.strip(),
            'footnote': current_footnote
        })
    
    return clauses

if __name__ == "__main__":
    debug_question_145() 