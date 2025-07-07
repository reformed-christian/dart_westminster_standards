#!/usr/bin/env python3

import fitz
import json
import re
import logging
from typing import Dict, List, Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WestminsterShorterCatechismExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = None
        self.footnotes = {}
        self.bold_flag = 16  # Bit 4 for bold text
        
    def open_pdf(self):
        """Open the PDF document"""
        try:
            self.doc = fitz.open(self.pdf_path)
            logger.info(f"Opened PDF with {len(self.doc)} pages")
        except Exception as e:
            logger.error(f"Failed to open PDF: {e}")
            raise
    
    def close_pdf(self):
        """Close the PDF document"""
        if self.doc:
            self.doc.close()
    
    def extract_text_from_pages(self, start_page: int, end_page: int) -> Tuple[str, List]:
        """Extract both plain text and structured text from specified pages"""
        plain_text = ""
        structured_data = []
        
        for page_num in range(start_page, min(end_page + 1, len(self.doc))):
            page = self.doc[page_num]
            
            # Get plain text
            page_text = page.get_text()
            plain_text += page_text + "\n"
            
            # Get structured text
            page_dict = page.get_text("dict")
            structured_data.append({
                'page': page_num,
                'blocks': page_dict.get('blocks', [])
            })
            
            logger.info(f"Extracted page {page_num}: {len(page_dict.get('blocks', []))} blocks")
        
        return plain_text, structured_data
    
    def find_footnote_boundaries(self, plain_text: str) -> List[Tuple[int, int]]:
        """Find the boundaries of each footnote in the plain text"""
        # Pattern to match footnote numbers (1, 2, 3, etc.) followed by space and a book name
        footnote_pattern = r'(\d+)\s+[A-Z][a-z]+'
        matches = list(re.finditer(footnote_pattern, plain_text))
        
        boundaries = []
        for i, match in enumerate(matches):
            start = match.start()
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(plain_text)
            boundaries.append((start, end))
        
        logger.info(f"Found {len(boundaries)} footnote boundaries")
        return boundaries
    
    def extract_bold_spans_from_blocks(self, blocks: List) -> List[Dict]:
        """Extract all bold spans from structured blocks"""
        bold_spans = []
        
        for block in blocks:
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    flags = span.get('flags', 0)
                    if flags & self.bold_flag:  # Check if bold
                        bold_spans.append({
                            'text': span.get('text', ''),
                            'font': span.get('font', ''),
                            'size': span.get('size', 0),
                            'flags': flags
                        })
        
        return bold_spans
    
    def combine_split_references(self, bold_spans: List[Dict]) -> List[str]:
        """Combine split references that appear in consecutive bold spans"""
        combined_references = []
        i = 0
        
        while i < len(bold_spans):
            current_text = bold_spans[i]['text'].strip()
            
            # Check if this is a book name (capital letter followed by lowercase)
            if re.match(r'^[A-Z][a-z]+$', current_text):
                # Look for the next bold span that might contain chapter:verse
                if i + 1 < len(bold_spans):
                    next_text = bold_spans[i + 1]['text'].strip()
                    # Check if next span contains chapter:verse pattern
                    if re.match(r'^\d+:\d+', next_text):
                        combined_ref = f"{current_text} {next_text}"
                        combined_references.append(combined_ref)
                        logger.info(f"Combined split reference: '{current_text}' + '{next_text}' = '{combined_ref}'")
                        i += 2  # Skip both spans
                        continue
            
            # If not a split reference, add as is
            if current_text:
                combined_references.append(current_text)
            i += 1
        
        return combined_references
    
    def complete_incomplete_references(self, references: List[str], regular_text: str) -> List[str]:
        """Complete references that are just book names by finding chapter:verse in following text"""
        completed_references = []
        
        for ref in references:
            # Check if this is just a book name
            if re.match(r'^[A-Z][a-z]+$', ref):
                # Look for chapter:verse pattern in the regular text
                chapter_verse_pattern = r'(\d+:\d+(?:-\d+)?(?:,\s*\d+(?::\d+)?)*)'
                match = re.search(chapter_verse_pattern, regular_text)
                if match:
                    completed_ref = f"{ref} {match.group(1)}"
                    completed_references.append(completed_ref)
                    logger.info(f"Completed incomplete reference: '{ref}' + '{match.group(1)}' = '{completed_ref}'")
                else:
                    completed_references.append(ref)
            else:
                completed_references.append(ref)
        
        return completed_references
    
    def clean_reference(self, reference: str) -> str:
        """Clean a reference by removing prefixes and normalizing"""
        # Remove common prefixes
        prefixes_to_remove = ['With ', 'Cf. ', 'See ']
        cleaned = reference
        for prefix in prefixes_to_remove:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
                logger.info(f"Removed prefix '{prefix}' from reference: '{reference}' -> '{cleaned}'")
                break
        
        # Remove trailing periods
        cleaned = cleaned.rstrip('.')
        
        return cleaned
    
    def extract_scripture_text(self, reference: str, footnote_text: str, ref_start_pos: int) -> str:
        """Extract the scripture text that follows a reference"""
        # Find the position of this reference in the footnote text
        ref_pos = footnote_text.find(reference, ref_start_pos)
        if ref_pos == -1:
            return ""
        
        # Find the next reference or end of footnote
        next_ref_pattern = r'\b[A-Z][a-z]+(?:\s+\d+:\d+)?\.'
        next_match = re.search(next_ref_pattern, footnote_text[ref_pos + len(reference):])
        
        if next_match:
            text_end = ref_pos + len(reference) + next_match.start()
        else:
            text_end = len(footnote_text)
        
        # Extract the text between reference and next reference/end
        scripture_text = footnote_text[ref_pos + len(reference):text_end].strip()
        
        # Clean up the text
        scripture_text = re.sub(r'\(\d+\)', '', scripture_text)  # Remove page numbers
        scripture_text = re.sub(r'\s+', ' ', scripture_text)  # Normalize whitespace
        scripture_text = scripture_text.strip()
        
        return scripture_text
    
    def extract_scripture_text_from_footnote(self, reference: str, footnote_text: str) -> str:
        """Extract the scripture text that follows a reference in a footnote"""
        # Find the reference in the footnote text
        ref_pos = footnote_text.find(reference)
        if ref_pos == -1:
            return ""
        
        # Look for the next reference pattern (book name followed by chapter:verse)
        next_ref_pattern = r'\b[A-Z][a-z]+(?:\s+\d+:\d+(?:-\d+)?(?:,\s*\d+(?::\d+)?)*)?\.'
        next_match = re.search(next_ref_pattern, footnote_text[ref_pos + len(reference):])
        
        if next_match:
            text_end = ref_pos + len(reference) + next_match.start()
        else:
            text_end = len(footnote_text)
        
        # Extract the text between reference and next reference/end
        scripture_text = footnote_text[ref_pos + len(reference):text_end].strip()
        
        # Clean up the text
        scripture_text = re.sub(r'\(\d+\)', '', scripture_text)  # Remove page numbers
        scripture_text = re.sub(r'\s+', ' ', scripture_text)  # Normalize whitespace
        scripture_text = scripture_text.strip()
        
        return scripture_text
    
    def process_footnote(self, footnote_num: int, footnote_text: str, structured_blocks: List) -> List[Dict]:
        """Process a single footnote to extract references and their text"""
        logger.info(f"Processing footnote {footnote_num}")
        
        # Extract all bold spans from this footnote's blocks
        bold_spans = self.extract_bold_spans_from_blocks(structured_blocks)
        logger.info(f"Found {len(bold_spans)} bold spans in footnote {footnote_num}")
        
        # Log all bold text for debugging
        for i, span in enumerate(bold_spans):
            logger.info(f"Bold span {i}: '{span['text']}' (font={span['font']}, size={span['size']}, flags={span['flags']})")
        
        # Combine split references
        references = self.combine_split_references(bold_spans)
        logger.info(f"After combining split references: {references}")
        
        # Complete incomplete references
        references = self.complete_incomplete_references(references, footnote_text)
        logger.info(f"After completing incomplete references: {references}")
        
        # Clean references
        cleaned_references = [self.clean_reference(ref) for ref in references]
        logger.info(f"After cleaning references: {cleaned_references}")
        
        # Remove duplicates (keep longer, more complete versions)
        unique_references = []
        for ref in cleaned_references:
            is_duplicate = False
            for existing_ref in unique_references:
                if ref in existing_ref or existing_ref in ref:
                    if len(ref) < len(existing_ref):
                        is_duplicate = True
                        logger.info(f"Removing shorter duplicate: '{ref}' (keeping '{existing_ref}')")
                    else:
                        # Replace shorter with longer
                        unique_references.remove(existing_ref)
                        logger.info(f"Replacing shorter reference: '{existing_ref}' with '{ref}'")
            if not is_duplicate:
                unique_references.append(ref)
        
        # Extract text for each reference using the actual text structure
        references_with_text = []
        
        for ref in unique_references:
            scripture_text = self.extract_scripture_text_from_footnote(ref, footnote_text)
            if scripture_text:
                references_with_text.append({
                    "reference": ref,
                    "text": scripture_text
                })
                logger.info(f"Associated text with reference '{ref}': '{scripture_text[:100]}...'")
            else:
                logger.warning(f"No text found for reference '{ref}' in footnote {footnote_num}")
        
        return references_with_text
    
    def extract_all_footnotes(self) -> Dict:
        """Extract all 227 footnotes from the PDF"""
        logger.info("Starting extraction of all footnotes")
        
        # Extract text from pages 17-54 (footnotes start on page 17, index 16)
        start_page = 16  # Page 17 (0-indexed)
        end_page = 53    # Page 54 (0-indexed)
        
        plain_text, structured_data = self.extract_text_from_pages(start_page, end_page)
        
        # Find footnote boundaries
        boundaries = self.find_footnote_boundaries(plain_text)
        
        # Process each footnote
        for i, (start, end) in enumerate(boundaries):
            footnote_num = i + 1
            if footnote_num > 227:  # Only process first 227 footnotes
                break
                
            footnote_text = plain_text[start:end]
            
            # Find corresponding structured blocks for this footnote
            # This is a simplified approach - in practice, you'd need more sophisticated mapping
            footnote_blocks = []
            for page_data in structured_data:
                for block in page_data['blocks']:
                    # Check if block contains text from this footnote
                    block_text = ""
                    for line in block.get('lines', []):
                        for span in line.get('spans', []):
                            block_text += span.get('text', '')
                    
                    if any(ref in block_text for ref in ['Psalm', 'Genesis', 'Matthew', 'John', 'Romans']):
                        footnote_blocks.append(block)
            
            # Process the footnote
            references = self.process_footnote(footnote_num, footnote_text, footnote_blocks)
            
            if references:
                self.footnotes[str(footnote_num)] = references
                logger.info(f"Processed footnote {footnote_num}: {len(references)} references")
            else:
                self.footnotes[str(footnote_num)] = []
                logger.warning(f"No references found for footnote {footnote_num}")
        
        return self.footnotes
    
    def save_to_json(self, output_path: str):
        """Save the extracted footnotes to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.footnotes, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(self.footnotes)} footnotes to {output_path}")
    
    def validate_extraction(self) -> bool:
        """Validate the extraction results"""
        logger.info("Validating extraction results")
        
        # Check that we have exactly 227 footnotes
        if len(self.footnotes) != 227:
            logger.error(f"Expected 227 footnotes, got {len(self.footnotes)}")
            return False
        
        # Check that all footnotes have at least one reference
        empty_footnotes = [num for num, refs in self.footnotes.items() if not refs]
        if empty_footnotes:
            logger.error(f"Empty footnotes found: {empty_footnotes}")
            return False
        
        # Check for "reference not found" entries
        for num, refs in self.footnotes.items():
            for ref in refs:
                if ref.get('reference') == 'reference not found':
                    logger.error(f"Found 'reference not found' in footnote {num}")
                    return False
                if not ref.get('text'):
                    logger.error(f"Empty text for reference '{ref.get('reference')}' in footnote {num}")
                    return False
        
        logger.info("Validation passed successfully")
        return True

def main():
    """Main extraction function"""
    extractor = WestminsterShorterCatechismExtractor('sources/Shorter_Catechism-prts.pdf')
    
    try:
        extractor.open_pdf()
        footnotes = extractor.extract_all_footnotes()
        
        # Validate the extraction
        if extractor.validate_extraction():
            # Save to JSON
            output_path = 'assets/catechisms/shorter/westminster_shorter_catechism_references_complete.json'
            extractor.save_to_json(output_path)
            print(f"Successfully extracted {len(footnotes)} footnotes to {output_path}")
        else:
            print("Extraction validation failed")
            
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise
    finally:
        extractor.close_pdf()

if __name__ == "__main__":
    main() 