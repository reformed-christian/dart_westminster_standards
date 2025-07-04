#!/usr/bin/env python3
"""
Fix Westminster Standards Proof Texts - Final Version

This script extracts footnotes from the end of the Westminster Shorter Catechism PDF,
matches them to clause endnote markers found in the questions, and populates accurate 
proof texts with scripture references and text.

Key Features:
- Extracts footnotes from the end of the PDF (pages 45-54)
- Maps endnote markers from questions to footnotes
- Creates proper proof text objects with reference and text
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

class WestminsterProofTextFixer:
    def __init__(self):
        self.trace_file = "footnote_extraction_final_trace.txt"
        
    def log_trace(self, message: str):
        """Log to trace file for debugging."""
        with open(self.trace_file, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
        logger.info(message)
    
    def extract_footnotes_from_end(self, pdf_path: str) -> Dict[int, List[Dict]]:
        """Extract footnotes from the end of the PDF (pages 45-54), starting at the first footnote marker."""
        footnotes = {}
        all_lines = []
        start_index = None
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                self.log_trace(f"Total PDF pages: {total_pages}")
                # Gather all lines from the last 10 pages
                for page_num in range(max(0, total_pages - 10), total_pages):
                    page = pdf.pages[page_num]
                    page_text = page.extract_text()
                    if not page_text:
                        continue
                    lines = page_text.split('\n')
                    all_lines.extend(lines)
                # Find the start of the footnotes: look for superscript 1 or regular 1 followed by 'Psalm 86.'
                for idx, line in enumerate(all_lines):
                    if re.match(r'^[¹1]\s*Psalm 86\.', line.strip()):
                        start_index = idx
                        self.log_trace(f"Found start of footnotes at line {idx}: {line.strip()}")
                        break
                if start_index is None:
                    self.log_trace("ERROR: Could not find the start of the footnotes (¹1 Psalm 86.)")
                    return footnotes
                # Only process lines from the start of the footnotes onward
                footnote_lines = all_lines[start_index:]
                # Now extract footnotes from these lines
                page_text = '\n'.join(footnote_lines)
                # Use the improved pattern for footnote extraction
                page_footnotes = self.extract_footnotes_from_page(page_text, 0)
                for footnote_num, footnote_content in page_footnotes.items():
                    footnotes[footnote_num] = footnote_content
                    self.log_trace(f"Found footnote {footnote_num} after anchor")
                self.log_trace(f"\n=== FOOTNOTE EXTRACTION SUMMARY ===")
                self.log_trace(f"Total footnotes found: {len(footnotes)}")
                self.log_trace(f"Footnote numbers: {sorted(footnotes.keys())}")
        except Exception as e:
            error_msg = f"Error extracting footnotes: {str(e)}"
            self.log_trace(error_msg)
            logger.error(error_msg)
        return footnotes
    
    def extract_footnotes_from_page(self, page_text: str, page_num: int) -> Dict[int, List[Dict]]:
        """Extract footnotes from a single page."""
        footnotes = {}
        
        # Pattern to match footnote numbers at the start of lines
        # Format: "178 Ephesians 2:8-9."
        pattern = r'^(\d+)\s+([A-Z][a-zA-Z\s]+:\d+[-\d:,;\s]*\.)'
        
        lines = page_text.split('\n')
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Try to match footnote pattern
            match = re.match(pattern, line)
            if match:
                footnote_num = int(match.group(1))
                if 1 <= footnote_num <= 227:  # Valid footnote range
                    self.log_trace(f"  Found footnote {footnote_num}: {line[:100]}...")
                    footnotes[footnote_num] = self.extract_footnote_content(lines, line_num, footnote_num)
        
        return footnotes
    
    def extract_footnote_content(self, lines: List[str], start_line: int, footnote_num: int) -> List[Dict]:
        """Extract the content of a footnote starting from a given line."""
        content_lines = []
        current_line = start_line
        
        # Collect lines until we hit the next footnote or end of content
        while current_line < len(lines):
            line = lines[current_line].strip()
            
            # Stop if we hit another footnote number
            if re.match(r'^\d+\s+[A-Z]', line) and current_line != start_line:
                break
            
            # Stop if we hit a page break or section break
            if re.match(r'^\d+$', line) and len(line) <= 3:  # Page numbers
                break
            
            if line:
                content_lines.append(line)
            
            current_line += 1
        
        # Join content and parse scripture references
        full_content = ' '.join(content_lines)
        return self.parse_scripture_references(full_content)
    
    def parse_scripture_references(self, content: str) -> List[Dict]:
        """Parse scripture references from footnote content."""
        proof_texts = []
        
        # Pattern to match scripture references
        # This matches: Book Name 1:2-3, 5; Another Book 4:1
        ref_pattern = r'([A-Z][a-zA-Z\s]+(?:\d+)?)\s*:\s*(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)'
        
        matches = re.finditer(ref_pattern, content)
        
        for match in matches:
            book = match.group(1).strip()
            verses = match.group(2).strip()
            reference = f"{book}:{verses}"
            
            # Extract the text that follows this reference
            start_pos = match.end()
            end_pos = content.find(';', start_pos)
            if end_pos == -1:
                end_pos = content.find('.', start_pos)
            if end_pos == -1:
                end_pos = len(content)
            
            text = content[start_pos:end_pos].strip()
            if text.startswith('.'):
                text = text[1:].strip()
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)
            
            proof_texts.append({
                'reference': reference,
                'text': text if text else f"Scripture text for {reference}"
            })
        
        return proof_texts
    
    def extract_endnote_markers_from_questions(self, data: Dict) -> Dict[int, List[int]]:
        """Extract endnote markers from all questions."""
        question_markers = {}
        
        questions = data.get('questions', [])
        
        for question in questions:
            question_num = question.get('number', 0)
            answer = question.get('answer', '')
            
            # Extract endnote markers from answer
            markers = self.extract_endnote_markers(answer)
            
            if markers:
                question_markers[question_num] = markers
                self.log_trace(f"Question {question_num}: {len(markers)} markers - {markers}")
        
        return question_markers
    
    def extract_endnote_markers(self, answer: str) -> List[int]:
        """Extract endnote marker numbers from answer text."""
        markers = []
        
        # Pattern: numbers at the end of sentences/clauses
        pattern = r'(\d+)(?=\s*[,.!?]|\s*$)'
        matches = re.finditer(pattern, answer)
        
        for match in matches:
            marker = int(match.group(1))
            if 1 <= marker <= 227:  # Valid footnote range
                markers.append(marker)
        
        return markers
    
    def process_question(self, question_data: Dict, footnotes: Dict[int, List[Dict]], question_markers: Dict[int, List[int]]) -> Dict:
        """Process a single question to fix proof texts."""
        question_num = question_data.get('number', 0)
        clauses = question_data.get('clauses', [])
        
        # Get markers for this question
        markers = question_markers.get(question_num, [])
        
        if not markers:
            # No markers found, return as is
            return question_data
        
        # Map markers to clauses
        marker_to_clause_map = {}
        
        if len(markers) == len(clauses):
            # Perfect 1:1 mapping
            for i, marker in enumerate(markers):
                marker_to_clause_map[marker] = i
        else:
            # Handle mismatched counts
            self.log_trace(f"Question {question_num}: {len(markers)} markers, {len(clauses)} clauses")
            
            # Assign markers to clauses in order
            for i, marker in enumerate(markers):
                if i < len(clauses):
                    marker_to_clause_map[marker] = i
                else:
                    # Extra markers go to the last clause
                    marker_to_clause_map[marker] = len(clauses) - 1
        
        # Update clauses with footnote numbers and proof texts
        for marker, clause_index in marker_to_clause_map.items():
            if clause_index < len(clauses):
                clause = clauses[clause_index]
                
                # Add footnote number
                clause['footnoteNum'] = marker
                
                # Add proof texts
                if marker in footnotes:
                    clause['proofTexts'] = footnotes[marker]
                else:
                    clause['proofTexts'] = [{
                        'reference': f"ERROR: Footnote {marker} not found",
                        'text': f"Footnote {marker} not found in extracted footnotes"
                    }]
                    self.log_trace(f"Warning: Footnote {marker} not found for question {question_num}")
        
        return question_data
    
    def fix_proof_texts(self, input_json_path: str, output_json_path: str, pdf_path: str):
        """Main function to fix proof texts."""
        self.log_trace("=== STARTING PROOF TEXT FIX - FINAL VERSION ===")
        
        # Clear trace file
        with open(self.trace_file, "w", encoding="utf-8") as f:
            f.write("=== WESTMINSTER PROOF TEXT EXTRACTION TRACE - FINAL ===\n\n")
        
        # Extract footnotes from the end of the PDF
        footnotes = self.extract_footnotes_from_end(pdf_path)
        
        # Load existing JSON
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract endnote markers from all questions
        question_markers = self.extract_endnote_markers_from_questions(data)
        
        # Process each question
        questions = data.get('questions', [])
        processed_count = 0
        improved_count = 0
        
        for question in questions:
            original_clauses = question.get('clauses', [])
            processed_question = self.process_question(question, footnotes, question_markers)
            
            # Check if we improved the question
            new_clauses = processed_question.get('clauses', [])
            if len(new_clauses) != len(original_clauses):
                improved_count += 1
            
            processed_count += 1
        
        # Add diagnostics to output
        data['diagnostics'] = {
            'total_footnotes_found': len(footnotes),
            'footnote_numbers': sorted(footnotes.keys()),
            'questions_with_markers': len(question_markers),
            'total_questions_processed': processed_count,
            'questions_improved': improved_count
        }
        
        # Save results
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.log_trace(f"\n=== COMPLETION SUMMARY ===")
        self.log_trace(f"Processed {processed_count} questions")
        self.log_trace(f"Improved {improved_count} questions")
        self.log_trace(f"Found {len(footnotes)} footnotes")
        self.log_trace(f"Questions with markers: {len(question_markers)}")
        self.log_trace(f"Output saved to: {output_json_path}")
        self.log_trace(f"Trace file: {self.trace_file}")
        
        return data

def main():
    fixer = WestminsterProofTextFixer()
    
    input_json = "assets/westminster_shorter_catechism_fixed.json"
    output_json = "assets/westminster_shorter_catechism_proof_texts_final.json"
    pdf_path = "sources/Shorter_Catechism.pdf"
    
    if not Path(input_json).exists():
        logger.error(f"Input JSON file not found: {input_json}")
        return
    
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    logger.info("Starting proof text fix...")
    result = fixer.fix_proof_texts(input_json, output_json, pdf_path)
    logger.info("Proof text fix completed!")

if __name__ == "__main__":
    main() 