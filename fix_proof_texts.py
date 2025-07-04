#!/usr/bin/env python3
"""
Fix Westminster Standards Proof Texts

This script extracts footnotes from the end of the Westminster Shorter Catechism PDF,
matches them to clause endnote markers, and populates accurate proof texts with
scripture references and text from the KJV source.

The issue: After fixing clause parsing, the proof texts are no longer accurate
because they don't match the new clause structure. Each clause's endnote marker
corresponds to a footnote number that contains the relevant scripture references.
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

class ProofTextFixer:
    def __init__(self):
        # Cache for PDF text and footnotes
        self.pdf_text = ""
        self.footnotes = {}
        self.kjv_data = {}
        
        # Endnote marker pattern (numbers after punctuation)
        self.marker_pattern = r'(?<=[\.\,\;\:])\s*(\d+)'
        
        # Footnote pattern (number followed by scripture references)
        self.footnote_pattern = r'(\d+)\.\s*(.*?)(?=\d+\.|$)'
        
        # Scripture reference patterns
        self.scripture_patterns = [
            # Full book name with chapter:verse
            r'([A-Za-z]+)\s+(\d+):(\d+(?:-\d+)?)',
            # Abbreviated book names
            r'([A-Za-z]{2,4})\.?\s+(\d+):(\d+(?:-\d+)?)',
            # Chapter only references
            r'([A-Za-z]+)\s+(\d+)',
        ]
    
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
    
    def load_kjv_data(self, kjv_path: str = "sources/kjv.json"):
        """Load KJV scripture data."""
        try:
            with open(kjv_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract verses from the structure
            rows = data.get("resultset", {}).get("row", [])
            
            for row in rows:
                field = row.get("field", [])
                if len(field) >= 5:
                    verse_id, book_num, chapter, verse, text = field
                    key = f"{book_num:02d}{chapter:03d}{verse:03d}"
                    self.kjv_data[key] = {
                        "book": int(book_num),
                        "chapter": int(chapter),
                        "verse": int(verse),
                        "text": text
                    }
            
            logger.info(f"Loaded {len(self.kjv_data)} KJV verses")
            
        except Exception as e:
            logger.error(f"Error loading KJV data: {e}")
    
    def extract_footnotes(self, pdf_text: str) -> Dict[int, List[str]]:
        """Extract footnotes from the end of the PDF text."""
        if self.footnotes:  # Return cached footnotes
            return self.footnotes
            
        # Look for footnotes section (usually at the end)
        # Try to find where footnotes start
        footnote_sections = [
            "Footnotes",
            "NOTES",
            "References",
            "Scripture References"
        ]
        
        footnote_start = -1
        for section in footnote_sections:
            pos = pdf_text.find(section)
            if pos != -1:
                footnote_start = pos
                break
        
        if footnote_start == -1:
            # Try to find by looking for patterns like "1. Genesis 1:1"
            matches = list(re.finditer(r'^\d+\.\s+[A-Z]', pdf_text, re.MULTILINE))
            if matches:
                footnote_start = matches[0].start()
        
        if footnote_start == -1:
            logger.warning("Could not find footnotes section")
            return {}
        
        # Extract footnotes text
        footnotes_text = pdf_text[footnote_start:]
        logger.info(f"Found footnotes starting at position {footnote_start}")
        
        # Parse footnotes
        footnotes = {}
        matches = re.finditer(self.footnote_pattern, footnotes_text, re.DOTALL)
        
        for match in matches:
            footnote_num = int(match.group(1))
            footnote_content = match.group(2).strip()
            
            # Extract scripture references from footnote content
            references = self.extract_scripture_references(footnote_content)
            if references:
                footnotes[footnote_num] = references
                logger.debug(f"Footnote {footnote_num}: {len(references)} references")
        
        self.footnotes = footnotes
        logger.info(f"Extracted {len(footnotes)} footnotes")
        return footnotes
    
    def extract_scripture_references(self, footnote_content: str) -> List[str]:
        """Extract scripture references from footnote content."""
        references = []
        
        # Split by common separators
        parts = re.split(r'[;,]', footnote_content)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Try to match scripture reference patterns
            for pattern in self.scripture_patterns:
                match = re.search(pattern, part)
                if match:
                    # Reconstruct the reference in standard format
                    book = match.group(1)
                    chapter = match.group(2)
                    verse = match.group(3) if len(match.groups()) > 2 else ""
                    
                    if verse:
                        reference = f"{book} {chapter}:{verse}"
                    else:
                        reference = f"{book} {chapter}"
                    
                    references.append(reference)
                    break
        
        return references
    
    def get_scripture_text(self, reference: str) -> Optional[str]:
        """Get scripture text for a given reference."""
        try:
            # Parse reference (simplified - you may need to enhance this)
            # Format: "Book Chapter:Verse" or "Book Chapter"
            match = re.match(r'([A-Za-z]+)\s+(\d+)(?::(\d+))?', reference)
            if not match:
                return None
            
            book_name = match.group(1).lower()
            chapter = int(match.group(2))
            verse = int(match.group(3)) if match.group(3) else 1
            
            # Simple book name mapping (you may want to use the full mapping from fetch_scriptures.py)
            book_mapping = {
                'genesis': 1, 'exodus': 2, 'leviticus': 3, 'numbers': 4, 'deuteronomy': 5,
                'joshua': 6, 'judges': 7, 'ruth': 8, '1samuel': 9, '2samuel': 10,
                '1kings': 11, '2kings': 12, '1chronicles': 13, '2chronicles': 14,
                'ezra': 15, 'nehemiah': 16, 'esther': 17, 'job': 18, 'psalm': 19, 'psalms': 19,
                'proverbs': 20, 'ecclesiastes': 21, 'song': 22, 'isaiah': 23, 'jeremiah': 24,
                'lamentations': 25, 'ezekiel': 26, 'daniel': 27, 'hosea': 28, 'joel': 29,
                'amos': 30, 'obadiah': 31, 'jonah': 32, 'micah': 33, 'nahum': 34,
                'habakkuk': 35, 'zephaniah': 36, 'haggai': 37, 'zechariah': 38, 'malachi': 39,
                'matthew': 40, 'mark': 41, 'luke': 42, 'john': 43, 'acts': 44,
                'romans': 45, '1corinthians': 46, '2corinthians': 47, 'galatians': 48,
                'ephesians': 49, 'philippians': 50, 'colossians': 51, '1thessalonians': 52,
                '2thessalonians': 53, '1timothy': 54, '2timothy': 55, 'titus': 56,
                'philemon': 57, 'hebrews': 58, 'james': 59, '1peter': 60, '2peter': 61,
                '1john': 62, '2john': 63, '3john': 64, 'jude': 65, 'revelation': 66
            }
            
            book_num = book_mapping.get(book_name)
            if not book_num:
                return None
            
            # Look up verse in KJV data
            key = f"{book_num:02d}{chapter:03d}{verse:03d}"
            verse_data = self.kjv_data.get(key)
            
            if verse_data:
                return verse_data["text"]
            else:
                logger.warning(f"Verse not found: {reference} (key: {key})")
                return None
                
        except Exception as e:
            logger.error(f"Error getting scripture text for {reference}: {e}")
            return None
    
    def extract_endnote_markers(self, text: str) -> List[Tuple[int, int]]:
        """Extract endnote markers and their positions from text."""
        markers = []
        for match in re.finditer(self.marker_pattern, text):
            marker_num = int(match.group(1))
            position = match.start()
            markers.append((marker_num, position))
        return markers
    
    def process_clause(self, clause_text: str, footnotes: Dict[int, List[str]]) -> Tuple[List[Dict], Optional[int]]:
        """Process a single clause to extract proof texts and footnote number."""
        # Find endnote markers in the clause
        markers = self.extract_endnote_markers(clause_text)
        
        if not markers:
            return [], None
        
        # Use the last marker in the clause (most common pattern)
        footnote_num = markers[-1][0]
        
        # Get scripture references for this footnote
        references = footnotes.get(footnote_num, [])
        
        # Create proof text objects
        proof_texts = []
        for reference in references:
            scripture_text = self.get_scripture_text(reference)
            if scripture_text:
                proof_texts.append({
                    "reference": reference,
                    "text": scripture_text
                })
            else:
                # Add error indicator
                proof_texts.append({
                    "reference": reference,
                    "text": "ERROR: Scripture text not found"
                })
        
        return proof_texts, footnote_num
    
    def process_question(self, question_data: Dict, footnotes: Dict[int, List[str]]) -> Dict:
        """Process a single question to fix proof texts."""
        clauses = question_data.get("clauses", [])
        answer = question_data.get("answer", "")
        
        # Extract all endnote markers from the answer
        answer_markers = self.extract_endnote_markers(answer)
        
        if not answer_markers:
            # No markers found, return as is
            return question_data
        
        # Map markers to clauses
        # Strategy: assign markers to clauses in order, with the last marker going to the last clause
        marker_to_clause_map = {}
        
        if len(answer_markers) == len(clauses):
            # Perfect 1:1 mapping
            for i, (marker_num, _) in enumerate(answer_markers):
                marker_to_clause_map[marker_num] = i
        elif len(answer_markers) < len(clauses):
            # Fewer markers than clauses - assign to first clauses
            for i, (marker_num, _) in enumerate(answer_markers):
                marker_to_clause_map[marker_num] = i
        else:
            # More markers than clauses - assign to clauses in order, last marker to last clause
            for i, (marker_num, _) in enumerate(answer_markers):
                if i < len(clauses) - 1:
                    marker_to_clause_map[marker_num] = i
                else:
                    # Last marker goes to last clause
                    marker_to_clause_map[marker_num] = len(clauses) - 1
        
        # Process each clause
        for clause_idx, clause in enumerate(clauses):
            # Find which markers belong to this clause
            clause_markers = [marker_num for marker_num, assigned_idx in marker_to_clause_map.items() 
                            if assigned_idx == clause_idx]
            
            if not clause_markers:
                # No markers for this clause
                clause["proofTexts"] = []
                continue
            
            # Use the first marker for this clause (or the only one)
            footnote_num = clause_markers[0]
            
            # Get scripture references for this footnote
            references = footnotes.get(footnote_num, [])
            
            # Create proof text objects
            proof_texts = []
            for reference in references:
                scripture_text = self.get_scripture_text(reference)
                if scripture_text:
                    proof_texts.append({
                        "reference": reference,
                        "text": scripture_text
                    })
                else:
                    # Add error indicator
                    proof_texts.append({
                        "reference": reference,
                        "text": "ERROR: Scripture text not found"
                    })
            
            # Update the clause
            clause["proofTexts"] = proof_texts
            clause["footnoteNum"] = footnote_num
        
        return question_data
    
    def fix_all_proof_texts(self, pdf_path: str, input_json_path: str, output_path: str):
        """Main function to fix all proof texts."""
        logger.info(f"Fixing proof texts for {input_json_path}")
        logger.info(f"Using PDF: {pdf_path}")
        
        # Load KJV data
        self.load_kjv_data()
        
        # Extract PDF text and footnotes
        pdf_text = self.extract_pdf_text(pdf_path)
        footnotes = self.extract_footnotes(pdf_text)
        
        if not footnotes:
            logger.error("No footnotes found - cannot proceed")
            return
        
        # Load existing JSON
        try:
            with open(input_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            return
        
        questions = data.get("questions", [])
        if not questions:
            logger.error("No questions found in JSON")
            return
        
        # Process each question
        processed_questions = []
        total_proof_texts = 0
        
        for question_data in questions:
            number = question_data.get("number")
            logger.info(f"Processing Q{number}...")
            
            # Process the question
            processed_question = self.process_question(question_data.copy(), footnotes)
            
            # Count proof texts
            question_proof_texts = 0
            for clause in processed_question.get("clauses", []):
                question_proof_texts += len(clause.get("proofTexts", []))
            
            total_proof_texts += question_proof_texts
            logger.info(f"Q{number}: {question_proof_texts} proof texts")
            
            processed_questions.append(processed_question)
        
        # Create output data
        output_data = {
            "title": data.get("title", "Westminster Shorter Catechism"),
            "year": data.get("year", 1647),
            "questions": processed_questions
        }
        
        # Save result
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Processed {len(processed_questions)} questions")
        logger.info(f"✅ Total proof texts: {total_proof_texts}")
        logger.info(f"✅ Saved to {output_path}")
        
        # Show sample of footnotes for verification
        logger.info("Sample footnotes:")
        for i, (num, refs) in enumerate(list(footnotes.items())[:5]):
            logger.info(f"  {num}: {refs}")

def main():
    fixer = ProofTextFixer()
    
    # File paths
    pdf_path = "sources/Shorter_Catechism.pdf"
    input_json = "assets/westminster_shorter_catechism_fixed.json"
    output_path = "assets/westminster_shorter_catechism_proof_texts_fixed.json"
    
    # Check if files exist
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if not Path(input_json).exists():
        logger.error(f"Input JSON not found: {input_json}")
        sys.exit(1)
    
    # Fix proof texts
    fixer.fix_all_proof_texts(pdf_path, input_json, output_path)

if __name__ == "__main__":
    main() 