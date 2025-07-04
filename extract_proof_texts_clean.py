#!/usr/bin/env python3
"""
Clean Proof Text Extraction for Westminster Shorter Catechism

Extracts footnotes from PDF and maps them to existing clauses without modifying clause structure.
"""

import json
import re
import fitz  # PyMuPDF
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CleanProofTextExtractor:
    def __init__(self):
        self.footnotes = {}
    
    def extract_footnotes_from_pdf(self, pdf_path: str) -> Dict[int, List[Dict]]:
        """Extract footnotes from PDF starting from page with marker (15)."""
        footnotes = {}
        
        try:
            doc = fitz.open(pdf_path)
            logger.info(f"PDF has {len(doc)} pages")
            
            # Find the first page where the top-of-page marker is (15)
            start_page = None
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                lines = text.splitlines()
                for line in lines[:5]:  # Check first 5 lines
                    if re.match(r"^\(\s*15\s*\)$", line.strip()):
                        start_page = page_num
                        logger.info(f"Found top-of-page marker (15) on PDF page {page_num+1}")
                        break
                if start_page is not None:
                    break
            
            if start_page is None:
                logger.error("Could not find page with top-of-page marker (15)")
                return {}
            
            # Extract footnotes from start_page onward
            logger.info(f"Extracting footnotes from PDF page {start_page+1} onward")
            current_footnote_num = None
            current_footnote_content = []
            
            for page_num in range(start_page, len(doc)):
                page = doc[page_num]
                text_dict = page.get_text("dict")
                
                # Process each text block
                for block in text_dict.get('blocks', []):
                    if block.get('type') == 0:  # Text block
                        for line in block.get('lines', []):
                            for span in line.get('spans', []):
                                font = span.get('font', 'unknown')
                                size = span.get('size', 0)
                                flags = span.get('flags', 0)
                                text = span.get('text', '')
                                
                                # Check if this is a new footnote number (small font, regular text)
                                if (size < 10 and re.match(r'^\s*\d+\s*$', text.strip())):
                                    # Save previous footnote
                                    if current_footnote_num is not None:
                                        content = " ".join(current_footnote_content).strip()
                                        footnotes[current_footnote_num] = self.parse_footnote_content(content)
                                    
                                    current_footnote_num = int(text.strip())
                                    current_footnote_content = []
                                else:
                                    # Add to current footnote content
                                    if current_footnote_num is not None:
                                        current_footnote_content.append(text)
            
            # Save the last footnote
            if current_footnote_num is not None:
                content = " ".join(current_footnote_content).strip()
                footnotes[current_footnote_num] = self.parse_footnote_content(content)
            
            logger.info(f"Extracted {len(footnotes)} footnotes total from page {start_page+1} onward")
            doc.close()
            return footnotes
            
        except Exception as e:
            logger.error(f"Error extracting footnotes: {e}")
            return {}
    
    def parse_footnote_content(self, content: str) -> List[Dict]:
        """Parse footnote content into proof text objects."""
        proof_texts = []
        
        # Split by common patterns that indicate new references
        # Look for patterns like "Psalm 68:18. Text here. Acts 1:11. More text."
        parts = re.split(r'(?=\b[A-Z][a-z]+(?:\s+\d+)?(?::\d+)?(?:\s*[-\d,]+)?(?:\s*[A-Z][a-z]+(?:\s+\d+)?(?::\d+)?)*\.)', content)
        
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
        
        return proof_texts
    
    def extract_footnote_markers(self, answer_text: str) -> List[int]:
        """Extract footnote markers from answer text."""
        markers = []
        # Pattern to find footnote markers (numbers that appear at the end of text or before spaces)
        matches = re.finditer(r'(\d+)(?=\s|$)', answer_text)
        
        for match in matches:
            marker_num = int(match.group(1))
            markers.append(marker_num)
        
        return markers
    
    def split_answer_into_clauses_with_markers(self, answer_text: str, markers: List[int]) -> List[Dict]:
        """Split answer into clauses based on footnote markers."""
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
                remaining_markers = self.extract_footnote_markers(remaining_text)
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
    
    def map_footnotes_to_clauses(self, questions: List[Dict], footnotes: Dict[int, List[Dict]]) -> List[Dict]:
        """Map extracted footnotes to clauses by extracting markers from answer text."""
        missing_footnotes = set()
        updated_clauses = 0
        
        for question in questions:
            answer = question.get("answer", "")
            
            # Extract footnote markers from answer
            markers = self.extract_footnote_markers(answer)
            
            # Split answer into clauses with markers
            clauses = self.split_answer_into_clauses_with_markers(answer, markers)
            
            # Map footnotes to clauses
            for clause in clauses:
                footnote_num = clause.get("footnoteNum")
                if footnote_num:
                    if footnote_num in footnotes:
                        clause["proofTexts"] = footnotes[footnote_num]
                        updated_clauses += 1
                    else:
                        clause["proofTexts"] = [{
                            "reference": "ERROR: Footnote not found", 
                            "text": f"Footnote {footnote_num} not found in extracted footnotes"
                        }]
                        missing_footnotes.add(footnote_num)
                else:
                    clause["proofTexts"] = []
            
            # Update question with new clauses
            question["clauses"] = clauses
        
        logger.info(f"Updated {updated_clauses} clauses with proof texts")
        logger.info(f"Missing footnotes: {sorted(list(missing_footnotes))}")
        
        return questions
    
    def process_catechism(self, pdf_path: str, input_json_path: str, output_path: str):
        """Main processing function."""
        logger.info("Starting clean proof text extraction")
        
        # Extract footnotes from PDF
        footnotes = self.extract_footnotes_from_pdf(pdf_path)
        if not footnotes:
            logger.error("No footnotes extracted from PDF")
            return
        
        # Load existing JSON with clauses
        try:
            with open(input_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading input JSON: {e}")
            return
        
        # Map footnotes to clauses
        questions = data.get("questions", [])
        logger.info(f"Processing {len(questions)} questions")
        
        updated_questions = self.map_footnotes_to_clauses(questions, footnotes)
        data["questions"] = updated_questions
        
        # Add diagnostics
        data["diagnostics"] = {
            "extracted_footnotes": len(footnotes),
            "footnote_range": f"{min(footnotes.keys()) if footnotes else 0} - {max(footnotes.keys()) if footnotes else 0}",
            "total_questions": len(questions)
        }
        
        # Save result
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved result to {output_path}")
        except Exception as e:
            logger.error(f"Error saving output: {e}")

def main():
    """Main function."""
    extractor = CleanProofTextExtractor()
    
    # File paths
    pdf_path = "sources/Shorter_Catechism.pdf"
    input_json_path = "assets/westminster_shorter_catechism.json"
    output_path = "assets/westminster_shorter_catechism_with_proof_texts.json"
    
    # Check if files exist
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    if not Path(input_json_path).exists():
        logger.error(f"Input JSON file not found: {input_json_path}")
        return
    
    # Process catechism
    extractor.process_catechism(pdf_path, input_json_path, output_path)
    
    logger.info("Clean proof text extraction completed")

if __name__ == "__main__":
    main() 