#!/usr/bin/env python3
"""
Fix Westminster Standards Clause Parsing

This script processes every question in the existing Westminster Shorter Catechism JSON,
identifies superscript endnote markers from the original PDF, and rebuilds the JSON 
structure with proper clause boundaries based on theological logic.

The issue: During PDF-to-JSON conversion, endnote markers indicating clause
boundaries were lost, causing complex answers to be dumped into single clauses
instead of being properly parsed into logical theological components.
"""

import json
import re
import PyPDF2
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WestminsterParser:
    def __init__(self):
        # Unicode superscript mapping
        self.superscript_map = {
            '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5',
            '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁰': '0'
        }
        
        # Regex patterns for different endnote marker formats
        self.marker_patterns = [
            # Unicode superscripts
            r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+',
            # Numbers after punctuation (common PDF extraction result)
            r'(?<=[\.\,\;\:])\s*\d+',
            # Bracketed numbers
            r'\[\d+\]',
            # Parenthetical numbers (but not verse references)
            r'(?<![A-Za-z])\(\d+\)(?![:\d])',
            # Caret notation
            r'\^\d+',
            # Small numbers at clause ends (heuristic)
            r'(?<=\w)\s+\d+(?=\s*[A-Z]|$)'
        ]
        
        # Cache for PDF text and detected patterns
        self.pdf_text = ""
        self.detected_pattern = None
        self.pdf_questions = {}
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        if self.pdf_text:  # Return cached text
            return self.pdf_text
            
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                self.pdf_text = text
                return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return ""
    
    def identify_marker_format(self, text: str) -> Optional[str]:
        """Identify which endnote marker format is used in the text."""
        if self.detected_pattern:  # Return cached pattern
            return self.detected_pattern
            
        for pattern in self.marker_patterns:
            matches = re.findall(pattern, text)
            if len(matches) > 10:  # Threshold for confidence
                logger.info(f"Detected marker pattern: {pattern}")
                logger.info(f"Sample matches: {matches[:5]}")
                self.detected_pattern = pattern
                return pattern
        
        logger.warning("No clear endnote marker pattern detected")
        return None
    
    def normalize_superscripts(self, text: str) -> str:
        """Convert Unicode superscripts to regular numbers."""
        for sup, num in self.superscript_map.items():
            text = text.replace(sup, num)
        return text
    
    def parse_clauses_from_text(self, answer_text: str, marker_pattern: str) -> List[str]:
        """Parse text into clauses based on endnote markers."""
        if not marker_pattern:
            return [answer_text.strip()]
        
        # Normalize text
        text = self.normalize_superscripts(answer_text)
        
        # Find all marker positions
        markers = []
        for match in re.finditer(marker_pattern, text):
            markers.append({
                'pos': match.start(),
                'end': match.end(),
                'marker': match.group()
            })
        
        if not markers:
            return [text.strip()]
        
        # Split into clauses
        clauses = []
        start_pos = 0
        
        for marker in markers:
            # Extract clause text (up to but not including the marker)
            clause_text = text[start_pos:marker['pos']].strip()
            if clause_text:
                clauses.append(clause_text)
            start_pos = marker['end']
        
        # Add remaining text after last marker
        remaining = text[start_pos:].strip()
        if remaining:
            clauses.append(remaining)
        
        return [clause for clause in clauses if clause]
    
    def extract_pdf_questions(self, pdf_path: str) -> Dict[int, Dict]:
        """Extract questions and answers from PDF text and cache them."""
        if self.pdf_questions:  # Return cached questions
            return self.pdf_questions
            
        text = self.extract_pdf_text(pdf_path)
        if not text:
            return {}
        
        # Pattern to match Q&A structure
        qa_pattern = r'Q\.\s*(\d+)\.\s*(.*?)\s*A\.\s*(.*?)(?=Q\.\s*\d+\.|$)'
        
        questions = {}
        matches = re.findall(qa_pattern, text, re.DOTALL)
        
        for number_str, question, answer in matches:
            try:
                number = int(number_str)
                
                # Clean up question and answer text
                question = re.sub(r'\s+', ' ', question.strip())
                answer = re.sub(r'\s+', ' ', answer.strip())
                
                questions[number] = {
                    "question": question,
                    "answer": answer
                }
                
            except ValueError:
                logger.warning(f"Could not parse question number: {number_str}")
                continue
        
        self.pdf_questions = questions
        return questions
    
    def load_existing_json(self, json_path: str) -> Dict:
        """Load existing JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading existing JSON: {e}")
            return {"questions": []}
    
    def process_single_question(self, question_data: Dict, pdf_questions: Dict[int, Dict], marker_pattern: str) -> Dict:
        """Process a single question and apply correct clause parsing."""
        number = question_data.get("number")
        existing_answer = question_data.get("answer", "")
        existing_clauses = question_data.get("clauses", [])
        
        # Try to get the original answer text from PDF
        pdf_answer = None
        if number in pdf_questions:
            pdf_answer = pdf_questions[number]["answer"]
        
        # Use PDF answer if available, otherwise use existing answer
        answer_to_parse = pdf_answer if pdf_answer else existing_answer
        
        # Parse answer into clauses
        if marker_pattern and answer_to_parse:
            new_clause_texts = self.parse_clauses_from_text(answer_to_parse, marker_pattern)
            
            # If we got multiple clauses, this is an improvement
            if len(new_clause_texts) > 1:
                logger.info(f"Q{number}: Improved from {len(existing_clauses)} to {len(new_clause_texts)} clauses")
                
                # Collect all existing proof texts
                all_existing_proofs = []
                for clause in existing_clauses:
                    all_existing_proofs.extend(clause.get("proofTexts", []))
                
                # Create new clause structure
                new_clauses = []
                for i, clause_text in enumerate(new_clause_texts):
                    # Put all proof texts on the first clause for now
                    # Could be made more sophisticated with semantic matching
                    proof_texts = all_existing_proofs if i == 0 else []
                    
                    new_clauses.append({
                        "text": clause_text,
                        "proofTexts": proof_texts
                    })
                
                # Update the question data
                question_data["clauses"] = new_clauses
                if pdf_answer:
                    question_data["answer"] = pdf_answer
                    
            else:
                # Single clause - check if we should update the answer text
                if pdf_answer and pdf_answer != existing_answer:
                    logger.info(f"Q{number}: Updated answer text from PDF")
                    question_data["answer"] = pdf_answer
                    if existing_clauses:
                        existing_clauses[0]["text"] = new_clause_texts[0]
        
        return question_data
    
    def analyze_question_87_specifically(self, text: str) -> Dict:
        """Specific analysis for the problematic Question 87."""
        # Look for Q87 specifically
        q87_pattern = r'Q\.\s*87\.\s*(.*?)\s*A\.\s*(.*?)(?=Q\.\s*88\.|$)'
        match = re.search(q87_pattern, text, re.DOTALL)
        
        if not match:
            return {}
        
        question, answer = match.groups()
        question = re.sub(r'\s+', ' ', question.strip())
        answer = re.sub(r'\s+', ' ', answer.strip())
        
        logger.info(f"Q87 Question: {question}")
        logger.info(f"Q87 Answer: {answer}")
        
        # Try different parsing approaches
        results = {}
        
        for i, pattern in enumerate(self.marker_patterns):
            clauses = self.parse_clauses_from_text(answer, pattern)
            results[f"pattern_{i}"] = {
                "pattern": pattern,
                "clause_count": len(clauses),
                "clauses": clauses
            }
        
        return results
    
    def process_all_questions(self, pdf_path: str, existing_json_path: str, output_path: str):
        """Main processing function - processes ALL questions in the existing JSON."""
        logger.info(f"Processing ALL questions from {existing_json_path}")
        logger.info(f"Using PDF reference: {pdf_path}")
        
        # Load existing JSON data
        existing_data = self.load_existing_json(existing_json_path)
        existing_questions = existing_data.get("questions", [])
        
        if not existing_questions:
            logger.error("No questions found in existing JSON file")
            return
        
        # Extract PDF questions for reference
        pdf_questions = self.extract_pdf_questions(pdf_path)
        logger.info(f"Found {len(pdf_questions)} questions in PDF for reference")
        
        # Identify marker pattern from PDF
        pdf_text = self.extract_pdf_text(pdf_path)
        marker_pattern = self.identify_marker_format(pdf_text)
        
        if not marker_pattern:
            logger.warning("No marker pattern detected - processing with existing structure")
        
        # Process each question
        processed_questions = []
        improvements = 0
        
        for question_data in existing_questions:
            number = question_data.get("number")
            original_clause_count = len(question_data.get("clauses", []))
            
            # Process the question
            processed_question = self.process_single_question(
                question_data.copy(), 
                pdf_questions, 
                marker_pattern
            )
            
            new_clause_count = len(processed_question.get("clauses", []))
            
            # Track improvements
            if new_clause_count > original_clause_count:
                improvements += 1
                logger.info(f"✓ Q{number}: {original_clause_count} → {new_clause_count} clauses")
            elif new_clause_count > 1:
                logger.debug(f"  Q{number}: Already had {new_clause_count} clauses")
            
            processed_questions.append(processed_question)
        
        # Create output data
        output_data = {
            "title": existing_data.get("title", "Westminster Shorter Catechism"),
            "year": existing_data.get("year", 1647),
            "questions": processed_questions
        }
        
        # Save result
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Processed {len(processed_questions)} questions total")
        logger.info(f"✅ Improved {improvements} questions with better clause parsing")
        logger.info(f"✅ Saved corrected catechism to {output_path}")
        
        # Special analysis for Q87
        q87_analysis = self.analyze_question_87_specifically(pdf_text)
        
        if q87_analysis:
            logger.info("=== Q87 Analysis ===")
            for key, result in q87_analysis.items():
                logger.info(f"{key}: {result['clause_count']} clauses")
                if result['clause_count'] > 1:
                    for i, clause in enumerate(result['clauses'], 1):
                        logger.info(f"  Clause {i}: {clause[:100]}...")

def main():
    parser = WestminsterParser()
    
    # File paths
    pdf_path = "sources/Shorter_Catechism.pdf"
    existing_json = "assets/westminster_shorter_catechism.json"
    output_path = "assets/westminster_shorter_catechism_fixed.json"
    
    # Check if files exist
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if not Path(existing_json).exists():
        logger.error(f"Existing JSON not found: {existing_json}")
        sys.exit(1)
    
    # Process all questions
    parser.process_all_questions(pdf_path, existing_json, output_path)

if __name__ == "__main__":
    main() 