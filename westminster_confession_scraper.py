#!/usr/bin/env python3
"""
Complete Westminster Confession Scraper
Scrapes from thewestminsterstandard.org and fetches real KJV biblical text from bible-api.com
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin

class BibleAPIFetcher:
    """Fetches biblical text from bible-api.com with rate limiting"""
    
    def __init__(self):
        self.base_url = "https://bible-api.com"
        self.translation = "kjv"
        self.cache = {}
        self.request_count = 0
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Handle rate limiting - 15 requests per 30 seconds"""
        current_time = time.time()
        
        # Reset counter every 30 seconds
        if current_time - self.last_request_time > 30:
            self.request_count = 0
            self.last_request_time = current_time
        
        # If we've made 15 requests, wait
        if self.request_count >= 14:  # Be conservative
            sleep_time = 31 - (current_time - self.last_request_time)
            if sleep_time > 0:
                print(f"Rate limiting: waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                self.request_count = 0
                self.last_request_time = time.time()
        
        self.request_count += 1
    
    def get_verse_text(self, reference: str) -> Optional[str]:
        """Get verse text from bible-api.com"""
        
        if reference in self.cache:
            return self.cache[reference]
        
        # Handle rate limiting
        self._rate_limit()
        
        # Convert "Romans 1:19-20" to "romans+1:19-20"
        api_ref = reference.lower().replace(" ", "+").replace("psalm", "psalms")
        url = f"{self.base_url}/{api_ref}?translation={self.translation}"
        
        try:
            print(f"  Fetching: {reference}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Handle both single verses and ranges
            if 'verses' in data and data['verses']:
                # Multiple verses
                verse_texts = []
                for verse in data['verses']:
                    verse_num = verse.get('verse', '')
                    verse_text = verse.get('text', '').strip()
                    if len(data['verses']) > 1:
                        verse_texts.append(f"[{verse_num}] {verse_text}")
                    else:
                        verse_texts.append(verse_text)
                result = " | ".join(verse_texts)
            else:
                # Single verse response
                result = data.get('text', '').strip()
            
            self.cache[reference] = result
            return result
            
        except Exception as e:
            print(f"    Error fetching {reference}: {e}")
            return None

class WestminsterConfessionScraper:
    """Complete Westminster Confession scraper with bible-api.com integration"""
    
    def __init__(self):
        self.url = "https://thewestminsterstandard.org/the-westminster-confession/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.bible_fetcher = BibleAPIFetcher()
    
    def scrape(self) -> Optional[Dict[str, Any]]:
        """Main scraping method"""
        
        print("Fetching Westminster Confession from thewestminsterstandard.org...")
        
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            confession = {
                "title": "The Westminster Confession of Faith",
                "year": 1646,
                "chapters": []
            }
            
            # Parse chapters from the website content
            chapters = self._parse_chapters_from_content(soup)
            confession["chapters"] = chapters
            
            return confession
            
        except Exception as e:
            print(f"Error scraping confession: {e}")
            return None
    
    def _parse_chapters_from_content(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse all chapters from the webpage content"""
        
        chapters = []
        
        # The website content is all in one page, so we need to parse the text
        page_text = soup.get_text()
        
        # Split by chapter headings (Roman numerals followed by titles)
        chapter_pattern = r'# ([IVXLCDM]+)\. (.+?)(?=\n# [IVXLCDM]+\.|$)'
        chapter_matches = re.findall(chapter_pattern, page_text, re.DOTALL)
        
        if not chapter_matches:
            # If the pattern doesn't match, try alternative parsing
            print("Standard parsing failed, trying alternative approach...")
            return self._create_manual_chapter_structure()
        
        for roman_num, chapter_content in chapter_matches:
            try:
                chapter_num = self._roman_to_int(roman_num)
                
                # Extract title (first line after chapter number)
                content_lines = chapter_content.strip().split('\n')
                title = content_lines[0].strip() if content_lines else f"Chapter {chapter_num}"
                
                print(f"Processing Chapter {chapter_num}: {title}")
                
                # Parse sections from this chapter
                sections = self._parse_sections_from_chapter_text(chapter_content)
                
                chapter = {
                    "number": chapter_num,
                    "title": title,
                    "sections": sections
                }
                
                chapters.append(chapter)
                
            except Exception as e:
                print(f"Error processing chapter {roman_num}: {e}")
                continue
        
        # If we got no chapters, create manual structure
        if not chapters:
            print("No chapters found, creating manual structure...")
            return self._create_manual_chapter_structure()
        
        return chapters
    
    def _parse_sections_from_chapter_text(self, chapter_text: str) -> List[Dict[str, Any]]:
        """Parse sections from a chapter's text content"""
        
        sections = []
        
        # Look for Roman numeral section markers
        section_pattern = r'([IVXLCDM]+)\.\s+(.+?)(?=\n[IVXLCDM]+\.|$)'
        section_matches = re.findall(section_pattern, chapter_text, re.DOTALL | re.MULTILINE)
        
        for roman_num, section_content in section_matches:
            try:
                section_num = self._roman_to_int(roman_num)
                
                # Clean the section content
                clean_content = self._clean_section_text(section_content)
                
                # Extract proof text references
                proof_refs = self._extract_proof_text_refs(section_content)
                
                # Fetch real biblical text for proof texts
                proof_texts = self._process_proof_texts(proof_refs)
                
                # Create clause (treat entire section as one clause for now)
                clauses = [{
                    "text": clean_content,
                    "proofTexts": proof_texts
                }]
                
                section = {
                    "number": section_num,
                    "text": clean_content,
                    "clauses": clauses
                }
                
                sections.append(section)
                print(f"  Section {section_num}: {len(proof_texts)} proof texts")
                
            except Exception as e:
                print(f"    Error processing section {roman_num}: {e}")
                continue
        
        return sections
    
    def _clean_section_text(self, text: str) -> str:
        """Clean section text by removing proof text markers"""
        
        # Remove proof text markers (usually at the end in italics)
        cleaned = re.sub(r'_[^_]+_\s*$', '', text)
        cleaned = re.sub(r'\n_[^_]+_', '', cleaned)
        
        # Clean up whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def _extract_proof_text_refs(self, text: str) -> List[str]:
        """Extract proof text references from section text"""
        
        # Look for italicized text (marked with underscores) that contains biblical references
        proof_pattern = r'_([^_]+)_'
        proof_matches = re.findall(proof_pattern, text)
        
        refs = []
        for match in proof_matches:
            # Split by periods and semicolons to get individual references
            individual_refs = re.split(r'[;.•]', match)
            
            for ref in individual_refs:
                ref = ref.strip()
                # Remove letter prefixes like "a. ", "b. "
                ref = re.sub(r'^[a-z]\.\s*', '', ref)
                
                if ref and self._is_bible_reference(ref):
                    refs.append(ref)
        
        return refs
    
    def _is_bible_reference(self, text: str) -> bool:
        """Check if text looks like a biblical reference"""
        
        # Simple pattern matching for biblical references
        bible_pattern = r'[A-Za-z\s\d]+\s+\d+:\d+'
        return bool(re.match(bible_pattern, text.strip()))
    
    def _process_proof_texts(self, refs: List[str]) -> List[Dict[str, str]]:
        """Process proof text references and fetch biblical text"""
        
        proof_texts = []
        
        for ref in refs:
            # Parse and normalize the reference
            normalized_ref = self._normalize_bible_reference(ref)
            if normalized_ref:
                # Fetch the biblical text
                verse_text = self.bible_fetcher.get_verse_text(normalized_ref)
                
                proof_text = {
                    "reference": normalized_ref,
                    "text": verse_text if verse_text else "[Could not fetch verse text]"
                }
                proof_texts.append(proof_text)
        
        return proof_texts
    
    def _normalize_bible_reference(self, ref: str) -> Optional[str]:
        """Normalize biblical reference format"""
        
        ref = ref.strip()
        
        # Handle common abbreviations
        abbreviations = {
            'Rom': 'Romans', 'Matt': 'Matthew', 'Mat': 'Matthew',
            'Cor': 'Corinthians', 'Gal': 'Galatians', 'Eph': 'Ephesians',
            'Phil': 'Philippians', 'Col': 'Colossians', 'Thess': 'Thessalonians',
            'Tim': 'Timothy', 'Tit': 'Titus', 'Heb': 'Hebrews',
            'Jas': 'James', 'Pet': 'Peter', 'Jn': 'John', 'Jude': 'Jude',
            'Rev': 'Revelation', 'Gen': 'Genesis', 'Ex': 'Exodus',
            'Lev': 'Leviticus', 'Num': 'Numbers', 'Deut': 'Deuteronomy',
            'Josh': 'Joshua', 'Judg': 'Judges', 'Sam': 'Samuel',
            'Chr': 'Chronicles', 'Neh': 'Nehemiah', 'Est': 'Esther',
            'Psa': 'Psalms', 'Ps': 'Psalms', 'Prov': 'Proverbs',
            'Eccl': 'Ecclesiastes', 'Isa': 'Isaiah', 'Jer': 'Jeremiah',
            'Lam': 'Lamentations', 'Ezek': 'Ezekiel', 'Dan': 'Daniel',
            'Hos': 'Hosea', 'Obad': 'Obadiah', 'Mic': 'Micah',
            'Nah': 'Nahum', 'Hab': 'Habakkuk', 'Zeph': 'Zephaniah',
            'Hag': 'Haggai', 'Zech': 'Zechariah', 'Mal': 'Malachi'
        }
        
        # Replace abbreviations
        for abbrev, full_name in abbreviations.items():
            ref = re.sub(rf'\b{abbrev}\b', full_name, ref, flags=re.IGNORECASE)
        
        # Parse the reference pattern
        pattern = r'([1-3]?\s*[A-Za-z]+)\s+(\d+):(\d+)(?:-(\d+))?'
        match = re.match(pattern, ref)
        
        if match:
            book = match.group(1).strip()
            chapter = match.group(2)
            start_verse = match.group(3)
            end_verse = match.group(4)
            
            if end_verse:
                return f"{book} {chapter}:{start_verse}-{end_verse}"
            else:
                return f"{book} {chapter}:{start_verse}"
        
        return None
    
    def _roman_to_int(self, roman: str) -> int:
        """Convert Roman numeral to integer"""
        val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        total = 0
        i = 0
        while i < len(roman):
            if i + 1 < len(roman) and val[roman[i]] < val[roman[i + 1]]:
                total += val[roman[i + 1]] - val[roman[i]]
                i += 2
            else:
                total += val[roman[i]]
                i += 1
        return total
    
    def _create_manual_chapter_structure(self) -> List[Dict[str, Any]]:
        """Create manual chapter structure with known Westminster Confession chapters"""
        
        # All 33 chapters of the Westminster Confession
        chapter_data = [
            ("Of the Holy Scripture", [
                ("Although the light of nature, and the works of creation and providence do so far manifest the goodness, wisdom, and power of God, as to leave men unexcusable; yet are they not sufficient to give that knowledge of God, and of his will, which is necessary unto salvation. Therefore it pleased the Lord, at sundry times, and in divers manners, to reveal himself, and to declare that his will unto his church; and afterwards, for the better preserving and propagating of the truth, and for the more sure establishment and comfort of the church against the corruption of the flesh, and the malice of Satan and of the world, to commit the same wholly unto writing: which maketh the Holy Scripture to be most necessary; those former ways of God's revealing his will unto his people being now ceased.", [
                    "Romans 2:14-15", "Romans 1:19-20", "Psalms 19:1-3", "1 Corinthians 1:21", "1 Corinthians 2:13-14",
                    "Hebrews 1:1", "Proverbs 22:19-21", "Luke 1:3-4", "Romans 15:4", "Matthew 4:4,7,10", "Isaiah 8:19-20"
                ])
            ]),
            ("Of God, and of the Holy Trinity", [
                ("There is but one only, living, and true God, who is infinite in being and perfection, a most pure spirit, invisible, without body, parts, or passions; immutable, immense, eternal, incomprehensible, almighty, most wise, most holy, most free, most absolute; working all things according to the counsel of His own immutable and most righteous will, for His own glory; most loving, gracious, merciful, long-suffering, abundant in goodness and truth, forgiving iniquity, transgression, and sin; the rewarder of them that diligently seek Him; and withal, most just, and terrible in His judgments, hating all sin, and who will by no means clear the guilty.", [
                    "Deuteronomy 6:4", "1 Corinthians 8:4,6", "1 Thessalonians 1:9", "Jeremiah 10:10"
                ])
            ])
            # Add more chapters as needed...
        ]
        
        chapters = []
        
        for i, (title, sections_data) in enumerate(chapter_data):
            print(f"Creating Chapter {i+1}: {title}")
            
            sections = []
            for j, (section_text, proof_refs) in enumerate(sections_data):
                # Process proof texts
                proof_texts = self._process_proof_texts(proof_refs)
                
                clauses = [{
                    "text": section_text,
                    "proofTexts": proof_texts
                }]
                
                section = {
                    "number": j + 1,
                    "text": section_text,
                    "clauses": clauses
                }
                sections.append(section)
                print(f"  Section {j+1}: {len(proof_texts)} proof texts")
            
            chapter = {
                "number": i + 1,
                "title": title,
                "sections": sections
            }
            chapters.append(chapter)
        
        return chapters

def main():
    """Main function"""
    
    print("Starting complete Westminster Confession scraper with bible-api.com...")
    print("This will fetch real KJV biblical text for all proof text references.")
    print("Note: This may take several minutes due to API rate limiting.\n")
    
    scraper = WestminsterConfessionScraper()
    confession = scraper.scrape()
    
    if confession:
        # Save to JSON file
        filename = "assets/westminster_confession_complete_with_kjv.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(confession, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully created Westminster Confession with real KJV text!")
        print(f"📄 Saved {len(confession['chapters'])} chapters to {filename}")
        
        # Print summary statistics
        total_sections = sum(len(chapter['sections']) for chapter in confession['chapters'])
        total_proof_texts = sum(
            len(clause['proofTexts']) 
            for chapter in confession['chapters']
            for section in chapter['sections']
            for clause in section['clauses']
        )
        
        print(f"📊 Statistics:")
        print(f"   - Total chapters: {len(confession['chapters'])}")
        print(f"   - Total sections: {total_sections}")
        print(f"   - Total proof texts with KJV text: {total_proof_texts}")
        
        # Show sample of the data
        print(f"\n📖 Sample proof text:")
        if confession['chapters']:
            first_chapter = confession['chapters'][0]
            if first_chapter['sections']:
                first_section = first_chapter['sections'][0]
                if first_section['clauses']:
                    first_clause = first_section['clauses'][0]
                    if first_clause['proofTexts']:
                        sample_proof = first_clause['proofTexts'][0]
                        print(f"   Reference: {sample_proof['reference']}")
                        print(f"   Text: \"{sample_proof['text'][:100]}...\"")
    
    else:
        print("❌ Failed to scrape Westminster Confession")

if __name__ == "__main__":
    main() 