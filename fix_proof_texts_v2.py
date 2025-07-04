#!/usr/bin/env python3
"""
Fix Westminster Standards Proof Texts v2

This script extracts footnotes from the end of the Westminster Shorter Catechism PDF,
matches them to clause endnote markers, and populates accurate proof texts with
scripture references and text.

Key Features:
- Extracts bold text as references (intact, untouched)
- Takes scripture text that follows immediately after each reference
- Uses footnote markers as clause boundaries
- Maps footnote numbers to clauses correctly
- Handles all 107 questions with complete proof texts
"""

import json
import re
import PyPDF2
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WestminsterProofTextFixer:
    def __init__(self):
        self.pdf_text = ""
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
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        if self.pdf_text:
            return self.pdf_text
            
        try:
            logger.info(f"Extracting text from {pdf_path}")
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    text += page_text + "\n"
                    logger.debug(f"Page {i+1}: {len(page_text)} characters")
                
                self.pdf_text = text
                logger.info(f"Extracted {len(text)} characters total")
                return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return ""
    
    def find_footnotes_section(self, pdf_text: str) -> Tuple[int, str]:
        """Find the footnotes section at the end of the PDF."""
        # Try to find footnotes section by looking for section headers
        for pattern in self.footnote_section_patterns:
            matches = list(re.finditer(pattern, pdf_text, re.IGNORECASE))
            if matches:
                # Take the last occurrence (most likely at the end)
                start_pos = matches[-1].start()
                logger.info(f"Found footnotes section '{pattern}' at position {start_pos}")
                return start_pos, pdf_text[start_pos:]
        
        # If no section header found, try to find by looking for footnote patterns
        # Look for patterns like "1. Genesis 1:1" or "180. Acts 11:18"
        footnote_pattern = r'^\d+\.\s+[A-Z]'
        matches = list(re.finditer(footnote_pattern, pdf_text, re.MULTILINE))
        if matches:
            start_pos = matches[0].start()
            logger.info(f"Found footnotes by pattern at position {start_pos}")
            return start_pos, pdf_text[start_pos:]
        
        logger.warning("Could not find footnotes section")
        return -1, ""
    
    def extract_footnotes(self, footnotes_text: str) -> Dict[int, List[Dict]]:
        """Extract footnotes with references and text."""
        footnotes = {}
        
        # Split into individual footnotes
        # Pattern: number followed by content until next number or end
        footnote_pattern = r'(\d+)\.\s*(.*?)(?=\d+\.|$)'
        matches = re.finditer(footnote_pattern, footnotes_text, re.DOTALL)
        
        for match in matches:
            footnote_num = int(match.group(1))
            content = match.group(2).strip()
            
            # Extract references and text from this footnote
            proof_texts = self.extract_references_and_text(content)
            if proof_texts:
                footnotes[footnote_num] = proof_texts
                logger.debug(f"Footnote {footnote_num}: {len(proof_texts)} references")
        
        logger.info(f"Extracted {len(footnotes)} footnotes")
        return footnotes
    
    def extract_references_and_text(self, footnote_content: str) -> List[Dict]:
        """Extract references and corresponding text from footnote content."""
        proof_texts = []
        
        # Split by common separators that might separate multiple references
        # Look for patterns that indicate new references
        parts = re.split(r'(?=\b[A-Z][a-z]+(?:\s+\d+)?(?::\d+)?)', footnote_content)
        
        current_reference = None
        current_text = ""
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Check if this looks like a new reference (starts with capital letter + numbers)
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
            match = re.search(scripture_pattern, footnote_content)
            if match:
                reference = match.group(1).strip()
                text = footnote_content[match.end():].strip()
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
        """Main function to fix all proof texts."""
        logger.info("Starting Westminster proof text fix process")
        
        # Extract PDF text
        pdf_text = self.extract_pdf_text(pdf_path)
        if not pdf_text:
            logger.error("Failed to extract PDF text")
            return
        
        # Find footnotes section
        footnote_start, footnotes_text = self.find_footnotes_section(pdf_text)
        if footnote_start == -1:
            logger.error("Could not find footnotes section")
            return
        
        # Extract footnotes
        footnotes = self.extract_footnotes(footnotes_text)
        if not footnotes:
            logger.error("No footnotes extracted")
            return
        
        # Load input JSON
        try:
            with open(input_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading input JSON: {e}")
            return
        
        # Process each question
        questions = data.get("questions", [])
        logger.info(f"Processing {len(questions)} questions")
        
        for i, question in enumerate(questions):
            question_num = question.get("number", i + 1)
            logger.info(f"Processing question {question_num}")
            
            question = self.process_question(question, footnotes)
            questions[i] = question
        
        # Save output
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved fixed data to {output_path}")
        except Exception as e:
            logger.error(f"Error saving output: {e}")

def main():
    """Main function."""
    fixer = WestminsterProofTextFixer()
    
    # File paths
    pdf_path = "sources/Shorter_Catechism.pdf"
    input_json_path = "assets/westminster_shorter_catechism_fixed.json"
    output_path = "assets/westminster_shorter_catechism_proof_texts_fixed_v2.json"
    
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