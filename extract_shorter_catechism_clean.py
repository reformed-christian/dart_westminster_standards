#!/usr/bin/env python3
"""
Clean extraction script following the step-by-step process:
1. Collect all text and clean up page breaks/numbers
2. Find all footnotes using font markers (must find exactly 227)
3. Extract references from each footnote
"""

import fitz
import json
import re
from typing import List, Dict

def debug_print_spans_on_page(pdf_path: str, page_num: int):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]
    print(f"\n--- Spans on page {page_num+1} ---")
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    print(f"Text: '{span['text']}' | Font: {span['font']} | Size: {span['size']} | Color: {span['color']} | Flags: {span['flags']}")

def step1_collect_and_clean_text(pdf_path: str, start_page: int = 16) -> str:
    """Step 1: Collect all text and clean up page breaks and numbers."""
    print("Step 1: Collecting and cleaning text...")
    
    doc = fitz.open(pdf_path)
    all_text = ""
    
    for page_num in range(start_page, len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        all_text += text + "\n"
    
    # Clean up the text
    # Remove page numbers (usually at bottom of page)
    all_text = re.sub(r'\n\d+\n', '\n', all_text)
    # Remove extra whitespace
    all_text = re.sub(r'\s+', ' ', all_text)
    # Clean up line breaks
    all_text = re.sub(r'\n+', '\n', all_text)
    
    print(f"Collected {len(all_text)} characters of text")
    return all_text

def step2_find_all_footnotes_perfect(pdf_path: str, start_page: int = 16) -> List[Dict]:
    """Step 2: Perfect font-based detection for footnotes."""
    print("Step 2: Perfect font-based detection for footnotes...")
    doc = fitz.open(pdf_path)
    footnotes = []
    last_footnote_num = 0
    for page_num in range(start_page, len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for i, span in enumerate(line["spans"]):
                        text = span["text"].strip()
                        # Criteria: Times-Roman, size ~7.92, color 9635840, flags 4, text is a single integer
                        if (
                            span["font"] == "Times-Roman"
                            and 7.5 < span["size"] < 8.5
                            and span["color"] == 9635840
                            and span["flags"] == 4
                            and text.isdigit()
                        ):
                            footnote_num = int(text)
                            # Check sequential
                            if footnote_num != last_footnote_num + 1:
                                print(f"WARNING: Footnote sequence break: got {footnote_num}, expected {last_footnote_num+1}")
                            last_footnote_num = footnote_num
                            # Collect text for this footnote
                            footnote_text = ""
                            # Get text from remaining spans in this line
                            for j in range(i + 1, len(line["spans"])):
                                footnote_text += line["spans"][j]["text"] + " "
                            # Get text from subsequent lines in this block
                            line_index = block["lines"].index(line)
                            for k in range(line_index + 1, len(block["lines"])):
                                for next_span in block["lines"][k]["spans"]:
                                    footnote_text += next_span["text"] + " "
                            # Get text from subsequent blocks until we hit another footnote or a paragraph break
                            block_index = blocks.index(block)
                            for m in range(block_index + 1, len(blocks)):
                                if "lines" in blocks[m]:
                                    for next_line in blocks[m]["lines"]:
                                        for next_span in next_line["spans"]:
                                            # Stop if we hit another footnote marker
                                            if (
                                                next_span["font"] == "Times-Roman"
                                                and 7.5 < next_span["size"] < 8.5
                                                and next_span["color"] == 9635840
                                                and next_span["flags"] == 4
                                                and next_span["text"].strip().isdigit()
                                            ):
                                                break
                                            footnote_text += next_span["text"] + " "
                                        else:
                                            continue
                                        break
                                else:
                                    continue
                                break
                            footnote_text = footnote_text.strip()
                            footnotes.append({
                                "number": footnote_num,
                                "text": footnote_text
                            })
    print(f"Found {len(footnotes)} footnotes")
    if len(footnotes) != 227:
        print(f"ERROR: Expected 227 footnotes, found {len(footnotes)}")
        print("Breaking as requested...")
        return []
    # Check for gaps in numbering
    numbers = [f["number"] for f in footnotes]
    expected_range = set(range(1, 228))
    found_set = set(numbers)
    missing = expected_range - found_set
    if missing:
        print(f"ERROR: Missing footnote numbers: {sorted(missing)}")
        return []
    print("✓ Successfully found all 227 footnotes")
    return footnotes

def step3_extract_references_from_footnotes_with_fonts(pdf_path: str, footnotes: List[Dict], start_page: int = 16) -> List[Dict]:
    """Step 3: Extract references using font information - all Times-Bold text."""
    print("Step 3: Extracting references using font information...")
    
    doc = fitz.open(pdf_path)
    references = []
    
    for footnote in footnotes:
        footnote_num = footnote["number"]
        
        # Find all Times-Bold spans in the footnote text
        bold_references = []
        
        for page_num in range(start_page, len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            # Check if this is a footnote number (our marker)
                            if (
                                span["font"] == "Times-Roman"
                                and 7.5 < span["size"] < 8.5
                                and span["color"] == 9635840
                                and span["flags"] == 4
                                and span["text"].strip().isdigit()
                                and int(span["text"].strip()) == footnote_num
                            ):
                                # Found our footnote, now collect all Times-Bold text and scripture text
                                current_ref = ""
                                current_scripture = ""
                                in_bold = False
                                last_span_end = span["bbox"][2]  # Track position for spacing
                                
                                # Get text from remaining spans in this line
                                span_index = line["spans"].index(span)
                                for i in range(span_index + 1, len(line["spans"])):
                                    next_span = line["spans"][i]
                                    
                                    # Add space if there's a gap between spans
                                    if next_span["bbox"][0] - last_span_end > 2:  # Gap larger than 2 points
                                        if in_bold:
                                            current_ref += " "
                                        else:
                                            current_scripture += " "
                                    
                                    if next_span["font"] == "Times-Bold":
                                        if current_ref and not in_bold:
                                            # Save previous reference and scripture
                                            ref = current_ref.rstrip('.')
                                            if ref:
                                                bold_references.append({
                                                    "reference": ref,
                                                    "scripture": current_scripture.strip()
                                                })
                                            current_ref = ""
                                            current_scripture = ""
                                        current_ref += next_span["text"]
                                        in_bold = True
                                    else:
                                        if in_bold:
                                            # End of bold text, start collecting scripture
                                            in_bold = False
                                        current_scripture += next_span["text"]
                                    
                                    last_span_end = next_span["bbox"][2]
                                
                                # Get text from subsequent lines in this block
                                line_index = block["lines"].index(line)
                                for k in range(line_index + 1, len(block["lines"])):
                                    next_line = block["lines"][k]
                                    # Add line break space
                                    if in_bold:
                                        current_ref += " "
                                    else:
                                        current_scripture += " "
                                    
                                    for next_span in next_line["spans"]:
                                        # Stop if we hit another footnote marker
                                        if (
                                            next_span["font"] == "Times-Roman"
                                            and 7.5 < next_span["size"] < 8.5
                                            and next_span["color"] == 9635840
                                            and next_span["flags"] == 4
                                            and next_span["text"].strip().isdigit()
                                        ):
                                            break
                                        
                                        # Add space if there's a gap
                                        if next_span["bbox"][0] - last_span_end > 2:
                                            if in_bold:
                                                current_ref += " "
                                            else:
                                                current_scripture += " "
                                        
                                        if next_span["font"] == "Times-Bold":
                                            if current_ref and not in_bold:
                                                # Save previous reference and scripture
                                                ref = current_ref.rstrip('.')
                                                if ref:
                                                    bold_references.append({
                                                        "reference": ref,
                                                        "scripture": current_scripture.strip()
                                                    })
                                                current_ref = ""
                                                current_scripture = ""
                                            current_ref += next_span["text"]
                                            in_bold = True
                                        else:
                                            if in_bold:
                                                # End of bold text, start collecting scripture
                                                in_bold = False
                                            current_scripture += next_span["text"]
                                        
                                        last_span_end = next_span["bbox"][2]
                                    else:
                                        continue
                                    break
                                
                                # Get text from subsequent blocks until we hit another footnote
                                block_index = blocks.index(block)
                                for m in range(block_index + 1, len(blocks)):
                                    if "lines" in blocks[m]:
                                        # Add paragraph break space
                                        if in_bold:
                                            current_ref += " "
                                        else:
                                            current_scripture += " "
                                        
                                        for next_line in blocks[m]["lines"]:
                                            for next_span in next_line["spans"]:
                                                # Stop if we hit another footnote marker
                                                if (
                                                    next_span["font"] == "Times-Roman"
                                                    and 7.5 < next_span["size"] < 8.5
                                                    and next_span["color"] == 9635840
                                                    and next_span["flags"] == 4
                                                    and next_span["text"].strip().isdigit()
                                                ):
                                                    break
                                                
                                                # Add space if there's a gap
                                                if next_span["bbox"][0] - last_span_end > 2:
                                                    if in_bold:
                                                        current_ref += " "
                                                    else:
                                                        current_scripture += " "
                                                
                                                if next_span["font"] == "Times-Bold":
                                                    if current_ref and not in_bold:
                                                        # Save previous reference and scripture
                                                        ref = current_ref.rstrip('.')
                                                        if ref:
                                                            bold_references.append({
                                                                "reference": ref,
                                                                "scripture": current_scripture.strip()
                                                            })
                                                        current_ref = ""
                                                        current_scripture = ""
                                                    current_ref += next_span["text"]
                                                    in_bold = True
                                                else:
                                                    if in_bold:
                                                        # End of bold text, start collecting scripture
                                                        in_bold = False
                                                    current_scripture += next_span["text"]
                                                
                                                last_span_end = next_span["bbox"][2]
                                            else:
                                                continue
                                            break
                                    else:
                                        continue
                                    break
                                
                                # Don't forget the last reference if it ends the footnote
                                if current_ref:
                                    ref = current_ref.rstrip('.')
                                    if ref:
                                        bold_references.append({
                                            "reference": ref,
                                            "scripture": current_scripture.strip()
                                        })
                                
                                # Add all references for this footnote
                                for ref_data in bold_references:
                                    references.append({
                                        "footnote_number": footnote_num,
                                        "reference": ref_data["reference"],
                                        "scripture_text": ref_data["scripture"]
                                    })
                                
                                # Break out of all loops since we found this footnote
                                break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue
            break
    
    print(f"Extracted {len(references)} references")
    return references

def main():
    pdf_path = "sources/Shorter_Catechism-prts.pdf"
    footnotes = step2_find_all_footnotes_perfect(pdf_path)
    if not footnotes:
        return
    # Step 3: Extract references using font information
    references = step3_extract_references_from_footnotes_with_fonts(pdf_path, footnotes)
    # Convert to output format
    output_references = {}
    for ref in references:
        key = str(ref["footnote_number"])
        entry = {
            "reference": ref["reference"],
            "text": ref["scripture_text"]
        }
        if key not in output_references:
            output_references[key] = []
        output_references[key].append(entry)
    # Save to JSON
    output_file = "westminster_shorter_catechism_references_clean.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_references, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {sum(len(v) for v in output_references.values())} references to {output_file}")
    print(f"Footnotes with references: {len(output_references)}")
    print(f"\nFirst 3 footnotes:")
    for k in sorted(output_references.keys(), key=lambda x: int(x))[:3]:
        print(f"  Footnote {k}: {len(output_references[k])} references")

if __name__ == "__main__":
    main() 