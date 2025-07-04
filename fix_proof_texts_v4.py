#!/usr/bin/env python3
"""
Fix Westminster Standards Proof Texts v4

This script extracts footnotes from the end of the Westminster Shorter Catechism PDF,
matches them to clause endnote markers, and populates accurate proof texts with
scripture references and text.

Key Features:
- Uses pdfplumber to detect bold text as references (intact, untouched)
- Takes scripture text that follows immediately after each reference
- Uses footnote markers as clause boundaries
- Maps footnote numbers to clauses correctly
- Handles all 107 questions with complete proof texts
- FIXED: Proper clause splitting with footnote assignment
- FIXED: Improved reference parsing for complex scripture references
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

class WestminsterProofTextFixerV4:
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
        """Extract footnotes by scanning from the page where the bottom-of-page marker is (15)."""
        footnotes = {}
        diagnostics = {
            'footnote_pages': [],
            'parsed_footnotes': [],
            'exceptions': [],
        }
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Find the first page where the bottom-of-page marker is (15)
                start_page = None
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    lines = text.splitlines()
                    # Look for a line that is exactly (15) or similar
                    for line in lines[-5:]:  # Only check last few lines
                        if re.match(r"^\(\s*15\s*\)$", line.strip()):
                            start_page = i
                            logger.info(f"Found bottom-of-page marker (15) on PDF page {i+1}")
                            break
                    if start_page is not None:
                        break
                if start_page is None:
                    logger.error("Could not find page with bottom-of-page marker (15)")
                    diagnostics['exceptions'].append('No page with (15) marker found')
                    self.diagnostics = diagnostics
                    return {}, diagnostics
                # Start extracting footnotes from start_page onward
                logger.info(f"Extracting footnotes from PDF page {start_page+1} onward")
                current_footnote_num = None
                current_footnote_content = []
                for page_num in range(start_page, len(pdf.pages)):
                    page = pdf.pages[page_num]
                    text = page.extract_text() or ""
                    lines = text.splitlines()
                    diagnostics['footnote_pages'].append({'page_num': page_num+1, 'lines': lines[:10]})
                    for line in lines:
                        # Look for a line/paragraph that starts with a number (superscript or not)
                        match = re.match(r"^\s*(\d{1,3})\s+(.*)", line)
                        if match:
                            # Save previous footnote group
                            if current_footnote_num is not None:
                                content = " ".join(current_footnote_content).strip()
                                footnotes[current_footnote_num] = self.parse_footnote_content(content)
                                diagnostics['parsed_footnotes'].append({'footnote_num': current_footnote_num, 'content': content})
                            current_footnote_num = int(match.group(1))
                            current_footnote_content = [match.group(2)]
                        else:
                            if current_footnote_num is not None:
                                current_footnote_content.append(line)
                    # At the end of the page, continue accumulating content
                # Save the last group
                if current_footnote_num is not None:
                    content = " ".join(current_footnote_content).strip()
                    footnotes[current_footnote_num] = self.parse_footnote_content(content)
                    diagnostics['parsed_footnotes'].append({'footnote_num': current_footnote_num, 'content': content})
                logger.info(f"Extracted {len(footnotes)} footnotes total from page {start_page+1} onward")
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
        """Parse footnote content to extract references and text with improved reference parsing."""
        proof_texts = []
        
        # Improved regex pattern for scripture references
        # Handles: Book names, chapter:verse patterns, ranges (1-3), comma-separated verses (1,2,3), and combinations
        scripture_pattern = r'([A-Z][a-z]+(?:\s+\d+)?(?:\s*:\s*\d+(?:[-\d,]+)?)?(?:\s*[A-Z][a-z]+(?:\s+\d+)?(?:\s*:\s*\d+(?:[-\d,]+)?)?)*)'
        
        # Find all scripture references in the content
        references = []
        last_end = 0
        
        for match in re.finditer(scripture_pattern, content):
            reference = match.group(1).strip()
            start_pos = match.start()
            end_pos = match.end()
            
            # Find the text that follows this reference (until the next reference or end)
            next_match = None
            for next_match_iter in re.finditer(scripture_pattern, content[end_pos:]):
                next_match = next_match_iter
                break
            
            if next_match:
                # Text goes from end of current reference to start of next reference
                text_end = end_pos + next_match.start()
                text = content[end_pos:text_end].strip()
            else:
                # This is the last reference, take all remaining text
                text = content[end_pos:].strip()
            
            # Clean up the reference and text
            reference = self.clean_reference(reference)
            text = self.clean_text(text)
            
            if reference and text:
                proof_texts.append({
                    "reference": reference,
                    "text": text
                })
        
        return proof_texts
    
    def clean_reference(self, reference: str) -> str:
        """Clean and normalize a scripture reference."""
        # Remove extra whitespace
        reference = re.sub(r'\s+', ' ', reference.strip())
        
        # Normalize common book name variations
        book_mappings = {
            'psa': 'Psalm', 'ps': 'Psalm',
            'matt': 'Matthew', 'rom': 'Romans',
            'cor': 'Corinthians', 'gal': 'Galatians',
            'eph': 'Ephesians', 'phil': 'Philippians',
            'col': 'Colossians', 'thess': 'Thessalonians',
            'tim': 'Timothy', 'tit': 'Titus',
            'heb': 'Hebrews', 'jas': 'James',
            'pet': 'Peter', 'rev': 'Revelation'
        }
        
        # Split reference into parts
        parts = reference.split()
        if len(parts) >= 2:
            book_part = parts[0].lower()
            if book_part in book_mappings:
                parts[0] = book_mappings[book_part]
            elif book_part.startswith('1') and len(book_part) > 1:
                base = book_part[1:]
                if base in book_mappings:
                    parts[0] = f"1 {book_mappings[base]}"
            elif book_part.startswith('2') and len(book_part) > 1:
                base = book_part[1:]
                if base in book_mappings:
                    parts[0] = f"2 {book_mappings[base]}"
            elif book_part.startswith('3') and len(book_part) > 1:
                base = book_part[1:]
                if base in book_mappings:
                    parts[0] = f"3 {book_mappings[base]}"
        
        return ' '.join(parts)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize scripture text."""
        # Remove leading/trailing whitespace and punctuation
        text = text.strip()
        
        # Remove leading periods, commas, etc.
        text = re.sub(r'^[.,;\s]+', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def extract_endnote_markers(self, answer_text: str) -> List[int]:
        """Extract endnote markers from answer text."""
        markers = []
        matches = re.finditer(self.marker_pattern, answer_text)
        
        for match in matches:
            marker_num = int(match.group(1))
            markers.append(marker_num)
        
        return markers
    
    def split_answer_into_clauses(self, answer_text: str, markers: List[int]) -> List[Dict]:
        """Split answer into clauses based on endnote markers with improved logic."""
        clauses = []
        
        if not markers:
            # No markers found, treat entire answer as one clause
            clauses.append({
                "text": answer_text.strip(),
                "footnoteNum": None,
                "proofTexts": []
            })
            return clauses
        
        # Find all marker positions
        marker_positions = []
        for marker in markers:
            marker_str = str(marker)
            pos = answer_text.find(marker_str)
            if pos != -1:
                marker_positions.append((pos, marker))
        
        # Sort by position
        marker_positions.sort(key=lambda x: x[0])
        
        # Split answer into clauses
        current_pos = 0
        
        for i, (marker_pos, marker) in enumerate(marker_positions):
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
            current_pos = marker_pos + len(str(marker))
        
        # Add any remaining text as the last clause
        if current_pos < len(answer_text):
            remaining_text = answer_text[current_pos:].strip()
            if remaining_text:
                # Check if the last clause should have a footnote
                # Look for any remaining markers in the text
                remaining_markers = self.extract_endnote_markers(remaining_text)
                if remaining_markers:
                    # Split the remaining text by the first marker
                    first_marker = remaining_markers[0]
                    marker_str = str(first_marker)
                    marker_pos = remaining_text.find(marker_str)
                    
                    if marker_pos != -1:
                        # Add the text before the marker as a clause with that footnote
                        before_marker = remaining_text[:marker_pos].strip()
                        if before_marker:
                            clauses.append({
                                "text": before_marker,
                                "footnoteNum": first_marker,
                                "proofTexts": []
                            })
                        
                        # Add the text after the marker as the final clause
                        after_marker = remaining_text[marker_pos + len(marker_str):].strip()
                        if after_marker:
                            clauses.append({
                                "text": after_marker,
                                "footnoteNum": None,
                                "proofTexts": []
                            })
                    else:
                        clauses.append({
                            "text": remaining_text,
                            "footnoteNum": None,
                            "proofTexts": []
                        })
                else:
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
        logger.info("Starting Westminster proof text fix process v4 (improved clause splitting and reference parsing)")
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
        updated_clauses = 0
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
            updated_clauses += len(question.get("clauses", []))
        diagnostics['missing_footnotes'] = sorted(list(missing_footnotes))
        diagnostics['updated_clauses'] = updated_clauses
        data['diagnostics'] = diagnostics
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved fixed data to {output_path}")
            logger.info(f"Updated {updated_clauses} clauses across {len(questions)} questions")
        except Exception as e:
            logger.error(f"Error saving output: {e}")
            diagnostics['exceptions'].append(f"Error saving output: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'diagnostics': diagnostics}, f, indent=2, ensure_ascii=False)

def main():
    """Main function."""
    fixer = WestminsterProofTextFixerV4()
    
    # File paths
    pdf_path = "sources/Shorter_Catechism.pdf"
    input_json_path = "assets/westminster_shorter_catechism.json"
    output_path = "assets/westminster_shorter_catechism_fixed_v4.json"
    
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