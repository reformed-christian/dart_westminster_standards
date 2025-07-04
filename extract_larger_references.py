import json
import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"
OUTPUT_PATH = "assets/westminster_larger_catechism_references.json"

MAX_FOOTNOTE = 500  # Adjust this based on actual number of footnotes

# Regex for a reference: starts with optional number, then book name, then chapter:verse, ends with a period
REFERENCE_REGEX = re.compile(r"^(?:[1-3] )?[A-Z][a-z]+(?: [A-Z][a-z]+)* ?\d*:?\d*(?:[-,\d: ]*)?\.$")

def extract_footnote_references(pdf_path):
    doc = fitz.open(pdf_path)
    # Start from page 42 (index 41)
    start_page = 41
    refs = {}
    current_footnote_num = None
    current_footnote_spans = []
    debug_count = 0
    
    for page_num in range(start_page, len(doc)):
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_flags = span.get('flags', 0)
                        is_bold = font_flags & 2**4  # Bold flag
                        
                        # Check if this is a footnote number
                        if text.isdigit() and 1 <= int(text) <= MAX_FOOTNOTE:
                            # Save previous footnote if exists
                            if current_footnote_num is not None:
                                refs[str(current_footnote_num)] = process_footnote_spans(current_footnote_spans)
                            
                            # Start new footnote
                            current_footnote_num = int(text)
                            current_footnote_spans = []
                            continue
                        
                        # Add span to current footnote
                        if current_footnote_num is not None:
                            current_footnote_spans.append({
                                'text': text,
                                'is_bold': is_bold
                            })
    
    # Save last footnote
    if current_footnote_num is not None:
        refs[str(current_footnote_num)] = process_footnote_spans(current_footnote_spans)
    
    # Fill in missing footnotes with empty lists
    for i in range(1, max(refs.keys(), default=0) + 1):
        if str(i) not in refs:
            refs[str(i)] = []
    
    return refs

def process_footnote_spans(spans):
    """Process spans to extract references and their corresponding text."""
    references = []
    current_reference = None
    current_text = []
    
    for span in spans:
        text = span['text']
        is_bold = span['is_bold']
        
        # Check if this bold text is a reference
        if is_bold and REFERENCE_REGEX.match(text):
            # Save previous reference if exists
            if current_reference is not None:
                references.append({
                    'reference': current_reference,
                    'text': ' '.join(current_text).strip()
                })
            
            # Start new reference
            current_reference = text.rstrip('.')  # Remove trailing period
            current_text = []
        else:
            # Add to current text
            if current_reference is not None:
                current_text.append(text)
    
    # Save last reference
    if current_reference is not None:
        references.append({
            'reference': current_reference,
            'text': ' '.join(current_text).strip()
        })
    
    return references

if __name__ == "__main__":
    print(f"Extracting footnote references from {PDF_PATH}...")
    references = extract_footnote_references(PDF_PATH)
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(references, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(references)} footnotes")
    print(f"Output written to: {OUTPUT_PATH}") 