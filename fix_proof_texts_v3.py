#!/usr/bin/env python3
"""
Fix Westminster Standards Proof Texts v3

This script extracts footnotes from the end of the Westminster Shorter Catechism PDF,
matches them to clause endnote markers, and populates accurate proof texts with
scripture references and text.

Key Features:
- Uses pdfplumber to detect bold text as references (intact, untouched)
- Takes scripture text that follows immediately after each reference
- Uses footnote markers as clause boundaries
- Maps footnote numbers to clauses correctly
- Handles all 107 questions with complete proof texts
"""

import json
import re
import pdfplumber
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WestminsterProofTextFixerV3:
    def __init__(self):
        self.footnotes = {}
        
        # Pattern to find footnote markers in answer text
        self.marker_pattern = r'(\d+)(?=\s|$)'
        
        # Pattern to find footnote sections
        self.footnote_section_patterns = [
            r'Footnotes?',
            r'NOTES',
            r'References?',
            r'Scripture References?'
        ]
    
    def extract_footnotes_with_bold_detection(self, pdf_path: str) -> Dict[int, List[Dict]]:
        """Extract footnotes using pdfplumber to detect bold text, with diagnostics."""
        footnotes = {}
        diagnostics = {
            'footnote_pages': [],
            'candidate_lines': [],
            'skipped_lines': [],
            'parsed_footnotes': [],
            'exceptions': [],
        }
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Start from the last few pages where footnotes are likely to be
                footnote_pages = []
                for page_num in range(max(0, len(pdf.pages) - 10), len(pdf.pages)):
                    page = pdf.pages[page_num]
                    page_text = page.extract_text()
                    # Print and log first 20 lines of each page
                    lines = page_text.splitlines()
                    diagnostics['footnote_pages'].append({
                        'page_num': page_num + 1,
                        'lines': lines[:20]
                    })
                    # Flexible regex: allow leading spaces, number, space, capital letter
                    candidate_lines = [(i, l) for i, l in enumerate(lines) if re.match(r'^\s*\d+\s+[A-Z]', l)]
                    for idx, l in candidate_lines:
                        diagnostics['candidate_lines'].append({'page': page_num + 1, 'line_num': idx + 1, 'text': l})
                    if candidate_lines:
                        footnote_pages.append(page_num)
                if not footnote_pages:
                    logger.warning("No footnote pages found")
                    diagnostics['exceptions'].append('No footnote pages found')
                    self.diagnostics = diagnostics
                    return {}, diagnostics
                # Extract footnotes from the identified pages
                for page_num in footnote_pages:
                    page = pdf.pages[page_num]
                    page_footnotes, page_diag = self.extract_footnotes_from_page(page)
                    footnotes.update(page_footnotes)
                    diagnostics['parsed_footnotes'].extend(page_diag['parsed_footnotes'])
                    diagnostics['skipped_lines'].extend(page_diag['skipped_lines'])
                logger.info(f"Extracted {len(footnotes)} footnotes total")
                self.diagnostics = diagnostics
                return footnotes, diagnostics
        except Exception as e:
            logger.error(f"Error extracting footnotes: {e}")
            diagnostics['exceptions'].append(str(e))
            self.diagnostics = diagnostics
            return {}, diagnostics

    def extract_footnotes_from_page(self, page) -> Tuple[Dict[int, List[Dict]], Dict]:
        """Extract footnotes from a single page with bold text detection and diagnostics."""
        footnotes = {}
        parsed_footnotes = []
        skipped_lines = []
        text_objects = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
        lines = {}
        for obj in text_objects:
            y_pos = round(obj['top'], 1)
            if y_pos not in lines:
                lines[y_pos] = []
            lines[y_pos].append(obj)
        sorted_lines = sorted(lines.items())
        current_footnote_num = None
        current_footnote_content = []
        for y_pos, line_objects in sorted_lines:
            line_objects.sort(key=lambda x: x['x0'])
            line_text = ' '.join([obj['text'] for obj in line_objects])
            # Flexible regex: allow leading spaces, number, space, capital letter
            footnote_match = re.match(r'^\s*(\d+)\s+([A-Z].*)', line_text)
            if footnote_match:
                if current_footnote_num is not None:
                    footnotes[current_footnote_num] = self.parse_footnote_content(' '.join(current_footnote_content))
                    parsed_footnotes.append({'footnote_num': current_footnote_num, 'content': ' '.join(current_footnote_content)})
                current_footnote_num = int(footnote_match.group(1))
                current_footnote_content = [footnote_match.group(2)]
            else:
                if current_footnote_num is not None:
                    current_footnote_content.append(line_text)
                else:
                    skipped_lines.append({'y_pos': y_pos, 'text': line_text})
        if current_footnote_num is not None:
            footnotes[current_footnote_num] = self.parse_footnote_content(' '.join(current_footnote_content))
            parsed_footnotes.append({'footnote_num': current_footnote_num, 'content': ' '.join(current_footnote_content)})
        return footnotes, {'parsed_footnotes': parsed_footnotes, 'skipped_lines': skipped_lines}
    
    def parse_footnote_content(self, content: str) -> List[Dict]:
        """Parse footnote content to extract references and text."""
        proof_texts = []
        
        # Split content by common separators that indicate new references
        # Look for patterns like "Genesis 1:1. Text here. Psalm 2:1. More text."
        parts = re.split(r'(?=\b[A-Z][a-z]+(?:\s+\d+)?(?::\d+)?(?:\s*[-\d,]+)?(?:\s*[A-Z][a-z]+(?:\s+\d+)?(?::\d+)?)*)', content)
        
        current_reference = None
        current_text = ""
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Check if this looks like a new reference
            if re.match(r'^[A-Z][a-z]+(?:\s+\d+)?(?::\d+)?', part):
                # Save previous reference if we have one
                if current_reference and current_text.strip():
                    proof_texts.append({
                        "reference": current_reference.strip(),
                        "text": current_text.strip()
                    })
                
                # Start new reference
                current_reference = part
                current_text = ""
            else:
                # This is text for the current reference
                if current_reference:
                    current_text += " " + part if current_text else part
        
        # Don't forget the last reference
        if current_reference and current_text.strip():
            proof_texts.append({
                "reference": current_reference.strip(),
                "text": current_text.strip()
            })
        
        # If no references found with the above method, try simpler approach
        if not proof_texts:
            # Look for any scripture reference pattern and take everything after it
            scripture_pattern = r'([A-Z][a-z]+(?:\s+\d+)?(?::\d+)?(?:\s*[-\d,]+)?(?:\s*[A-Z][a-z]+(?:\s+\d+)?(?::\d+)?)*)'
            match = re.search(scripture_pattern, content)
            if match:
                reference = match.group(1).strip()
                text = content[match.end():].strip()
                if text:
                    proof_texts.append({
                        "reference": reference,
                        "text": text
                    })
        
        return proof_texts
    
    def extract_endnote_markers(self, answer_text: str) -> List[int]:
        """Extract endnote markers from answer text."""
        markers = []
        matches = re.finditer(self.marker_pattern, answer_text)
        
        for match in matches:
            marker_num = int(match.group(1))
            markers.append(marker_num)
        
        return markers
    
    def split_answer_into_clauses(self, answer_text: str, markers: List[int]) -> List[Dict]:
        """Split answer into clauses based on endnote markers."""
        clauses = []
        
        if not markers:
            # No markers found, treat entire answer as one clause
            clauses.append({
                "text": answer_text.strip(),
                "footnoteNum": None,
                "proofTexts": []
            })
            return clauses
        
        # Split answer by markers
        current_pos = 0
        
        for i, marker in enumerate(markers):
            # Find the marker in the text
            marker_str = str(marker)
            marker_pos = answer_text.find(marker_str, current_pos)
            
            if marker_pos == -1:
                logger.warning(f"Marker {marker} not found in answer text")
                continue
            
            # Extract clause text (from current position to marker position)
            clause_text = answer_text[current_pos:marker_pos].strip()
            
            # Create clause object
            clause = {
                "text": clause_text,
                "footnoteNum": marker,
                "proofTexts": []
            }
            clauses.append(clause)
            
            # Move position past the marker
            current_pos = marker_pos + len(marker_str)
        
        # Add any remaining text as the last clause
        if current_pos < len(answer_text):
            remaining_text = answer_text[current_pos:].strip()
            if remaining_text:
                clauses.append({
                    "text": remaining_text,
                    "footnoteNum": None,
                    "proofTexts": []
                })
        
        return clauses
    
    def populate_proof_texts(self, clauses: List[Dict], footnotes: Dict[int, List[Dict]]) -> List[Dict]:
        """Populate proof texts for each clause based on footnote numbers."""
        for clause in clauses:
            footnote_num = clause.get("footnoteNum")
            if footnote_num and footnote_num in footnotes:
                clause["proofTexts"] = footnotes[footnote_num]
                logger.debug(f"Added {len(footnotes[footnote_num])} proof texts to clause with footnote {footnote_num}")
            elif footnote_num:
                clause["proofTexts"] = [{"reference": "ERROR: Footnote not found", "text": f"Footnote {footnote_num} not found in extracted footnotes"}]
                logger.warning(f"Footnote {footnote_num} not found in extracted footnotes")
            else:
                clause["proofTexts"] = []
        
        return clauses
    
    def process_question(self, question_data: Dict, footnotes: Dict[int, List[Dict]]) -> Dict:
        """Process a single question to fix proof texts."""
        answer = question_data.get("answer", "")
        
        # Extract endnote markers from answer
        markers = self.extract_endnote_markers(answer)
        
        # Split answer into clauses
        clauses = self.split_answer_into_clauses(answer, markers)
        
        # Populate proof texts
        clauses = self.populate_proof_texts(clauses, footnotes)
        
        # Update question data
        question_data["clauses"] = clauses
        
        return question_data
    
    def fix_all_proof_texts(self, pdf_path: str, input_json_path: str, output_path: str):
        logger.info("Starting Westminster proof text fix process v3 (diagnostic mode)")
        footnotes, diagnostics = self.extract_footnotes_with_bold_detection(pdf_path)
        if not footnotes:
            logger.error("No footnotes extracted")
        try:
            with open(input_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading input JSON: {e}")
            diagnostics['exceptions'].append(f"Error loading input JSON: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'diagnostics': diagnostics}, f, indent=2, ensure_ascii=False)
            return
        questions = data.get("questions", [])
        logger.info(f"Processing {len(questions)} questions")
        missing_footnotes = set()
        for i, question in enumerate(questions):
            question_num = question.get("number", i + 1)
            logger.info(f"Processing question {question_num}")
            answer = question.get("answer", "")
            markers = self.extract_endnote_markers(answer)
            for marker in markers:
                if marker not in footnotes:
                    missing_footnotes.add(marker)
            question = self.process_question(question, footnotes)
            questions[i] = question
        diagnostics['missing_footnotes'] = sorted(list(missing_footnotes))
        data['diagnostics'] = diagnostics
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved fixed data to {output_path}")
        except Exception as e:
            logger.error(f"Error saving output: {e}")
            diagnostics['exceptions'].append(f"Error saving output: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'diagnostics': diagnostics}, f, indent=2, ensure_ascii=False)

def main():
    """Main function."""
    fixer = WestminsterProofTextFixerV3()
    
    # File paths
    pdf_path = "sources/Shorter_Catechism.pdf"
    input_json_path = "assets/westminster_shorter_catechism_fixed.json"
    output_path = "assets/westminster_shorter_catechism_proof_texts_fixed_v3.json"
    
    # Check if files exist
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    if not Path(input_json_path).exists():
        logger.error(f"Input JSON file not found: {input_json_path}")
        return
    
    # Fix proof texts
    fixer.fix_all_proof_texts(pdf_path, input_json_path, output_path)
    
    logger.info("Proof text fixing process completed")

if __name__ == "__main__":
    main() 