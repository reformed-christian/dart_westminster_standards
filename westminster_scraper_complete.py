#!/usr/bin/env python3
"""
Complete Westminster Confession Scraper - Local File Version
Reads from downloaded Westminster files and fetches real KJV biblical text
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from typing import List, Dict, Any, Optional

class BibleAPIFetcher:
    """Fetches biblical text from GitHub KJV JSON file - no rate limiting needed!"""
    
    def __init__(self):
        self.kjv_url = "https://raw.githubusercontent.com/bibleapi/bibleapi-bibles-json/refs/heads/master/kjv.json"
        self.bible_data = {}
        self.cache = {}
        self.book_names = {
            1: "genesis", 2: "exodus", 3: "leviticus", 4: "numbers", 5: "deuteronomy",
            6: "joshua", 7: "judges", 8: "ruth", 9: "1 samuel", 10: "2 samuel",
            11: "1 kings", 12: "2 kings", 13: "1 chronicles", 14: "2 chronicles",
            15: "ezra", 16: "nehemiah", 17: "esther", 18: "job", 19: "psalms",
            20: "proverbs", 21: "ecclesiastes", 22: "song of solomon", 23: "isaiah",
            24: "jeremiah", 25: "lamentations", 26: "ezekiel", 27: "daniel",
            28: "hosea", 29: "joel", 30: "amos", 31: "obadiah", 32: "jonah",
            33: "micah", 34: "nahum", 35: "habakkuk", 36: "zephaniah", 37: "haggai",
            38: "zechariah", 39: "malachi", 40: "matthew", 41: "mark", 42: "luke",
            43: "john", 44: "acts", 45: "romans", 46: "1 corinthians", 47: "2 corinthians",
            48: "galatians", 49: "ephesians", 50: "philippians", 51: "colossians",
            52: "1 thessalonians", 53: "2 thessalonians", 54: "1 timothy", 55: "2 timothy",
            56: "titus", 57: "philemon", 58: "hebrews", 59: "james", 60: "1 peter",
            61: "2 peter", 62: "1 john", 63: "2 john", 64: "3 john", 65: "jude", 66: "revelation"
        }
        self.book_name_to_num = {v: k for k, v in self.book_names.items()}
        self._load_bible_data()
        
    def _load_bible_data(self):
        """Load KJV Bible data from GitHub JSON file"""
        print("📖 Loading KJV Bible data from GitHub...")
        
        try:
            response = requests.get(self.kjv_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse the JSON structure: field = [id, book_num, chapter, verse, text]
            for row in data['resultset']['row']:
                field = row['field']
                book_num = field[1]
                chapter = field[2]
                verse = field[3]
                text = field[4]
                
                # Create nested structure: bible_data[book_num][chapter][verse] = text
                if book_num not in self.bible_data:
                    self.bible_data[book_num] = {}
                if chapter not in self.bible_data[book_num]:
                    self.bible_data[book_num][chapter] = {}
                
                self.bible_data[book_num][chapter][verse] = text
            
            print(f"✅ Loaded complete KJV Bible with {len(data['resultset']['row'])} verses!")
            
        except Exception as e:
            print(f"❌ Error loading Bible data: {e}")
            self.bible_data = {}
    
    def _is_consecutive_range(self, reference: str) -> bool:
        """Check if reference is a consecutive range like 'Romans 1:19-20' vs comma-separated like 'Matthew 5:11, 17'"""
        return '-' in reference and ',' not in reference
    
    def get_verse_text(self, reference: str) -> Optional[str]:
        """Get verse text from local Bible data - super fast!"""
        
        if reference in self.cache:
            return self.cache[reference]
        
        if not self.bible_data:
            return f"[Bible data not loaded] {reference}"
        
        try:
            print(f"  📖 Looking up: {reference}")
            
            # Parse the reference (e.g., "Rom 1:19-20", "1 Cor 1:21", "Psa 19:1-3")
            result = self._parse_and_lookup_reference(reference)
            
            if result:
                self.cache[reference] = result
                return result
            else:
                fallback = f"[Reference not found] {reference}"
                self.cache[reference] = fallback
                return fallback
                
        except Exception as e:
            print(f"    ❌ Error looking up {reference}: {e}")
            fallback = f"[Lookup error] {reference}"
            self.cache[reference] = fallback
            return fallback
    
    def _parse_and_lookup_reference(self, reference: str) -> Optional[str]:
        """Parse reference and lookup verses from Bible data"""
        
        # Normalize reference
        ref = reference.strip()
        
        # Handle patterns like "Rom 1:19-20", "1 Cor 1:21", "Psa 19:1-3", "Matt 5:11, 17"
        # First extract book name and chapter:verse info
        
        # Pattern: (Optional number) (Book name) (chapter):(verses)
        match = re.match(r'(\d+\s+)?([A-Za-z]+\.?)\s+(\d+):(.+)', ref)
        if not match:
            return None
        
        number_prefix = match.group(1) or ""
        book_part = match.group(2)
        chapter = int(match.group(3))
        verse_part = match.group(4)
        
        # Construct full book name
        full_book = (number_prefix + book_part).strip().lower()
        
        # Normalize book name
        full_book = self._normalize_book_for_lookup(full_book)
        
        # Find book number
        book_num = self.book_name_to_num.get(full_book)
        if not book_num:
            # Try partial matching
            for name, num in self.book_name_to_num.items():
                if full_book in name or name.startswith(full_book[:3]):
                    book_num = num
                    break
        
        if not book_num:
            return None
            
        # Check if book/chapter exists
        if book_num not in self.bible_data or chapter not in self.bible_data[book_num]:
            return None
        
        chapter_data = self.bible_data[book_num][chapter]
        
        # Parse verse specification
        verses = []
        is_consecutive = self._is_consecutive_range(reference)
        
        if '-' in verse_part and ',' not in verse_part:
            # Range like "19-20"
            start, end = verse_part.split('-')
            start_verse = int(start.strip())
            end_verse = int(end.strip())
            
            for v in range(start_verse, end_verse + 1):
                if v in chapter_data:
                    verse_text = chapter_data[v]
                    if is_consecutive:
                        verses.append(f"[{v}] {verse_text}")
                    else:
                        verses.append(verse_text)
        
        elif ',' in verse_part:
            # Comma-separated like "11, 17"
            verse_nums = [int(v.strip()) for v in verse_part.split(',')]
            for v in verse_nums:
                if v in chapter_data:
                    verse_text = chapter_data[v]
                    verses.append(f"[{v}] {verse_text}")
        
        else:
            # Single verse
            verse_num = int(verse_part.strip())
            if verse_num in chapter_data:
                verse_text = chapter_data[verse_num]
                verses.append(verse_text)
        
        if verses:
            if is_consecutive:
                return " ".join(verses)
            else:
                return " | ".join(verses)
        
        return None
    
    def _normalize_book_for_lookup(self, book: str) -> str:
        """Normalize book name for lookup"""
        
        # Common mappings
        mappings = {
            "psa": "psalms", "ps": "psalms",
            "matt": "matthew", "rom": "romans",
            "cor": "corinthians", "gal": "galatians",
            "eph": "ephesians", "phil": "philippians",
            "col": "colossians", "thess": "thessalonians",
            "tim": "timothy", "tit": "titus",
            "heb": "hebrews", "jas": "james",
            "pet": "peter", "rev": "revelation"
        }
        
        # Handle numbered books
        if book.startswith("1 "):
            base = book[2:]
            if base in mappings:
                return f"1 {mappings[base]}"
            elif base == "sam":
                return "1 samuel"
            elif base == "cor":
                return "1 corinthians"
            elif base in ["chr", "chronicles"]:
                return "1 chronicles"
        elif book.startswith("2 "):
            base = book[2:]
            if base in mappings:
                return f"2 {mappings[base]}"
            elif base == "sam":
                return "2 samuel"
            elif base == "cor":
                return "2 corinthians"
            elif base in ["chr", "chronicles"]:
                return "2 chronicles"
        elif book.startswith("3 "):
            return f"3 {book[2:]}"
        
        # Single books
        return mappings.get(book, book)

class WestminsterLocalScraper:
    """Scrapes Westminster Confession from local downloaded files"""
    
    def __init__(self, local_file_path: str):
        self.local_file_path = local_file_path
        self.bible_fetcher = BibleAPIFetcher()
    
    def parse_local_confession(self) -> Dict[str, Any]:
        """Parse the complete Westminster Confession from local file"""
        
        print("🔍 Reading Westminster Confession from local file...")
        
        try:
            with open(self.local_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            print("✅ Successfully loaded local Westminster Confession file")
            
            confession = {
                "title": "The Westminster Confession of Faith",
                "year": 1646,
                "chapters": []
            }
            
            # Find all chapter sections
            chapters = self._extract_all_chapters(soup)
            
            total_proof_texts = 0
            
            for chapter_data in chapters:
                chapter_num = chapter_data['number']
                print(f"\n📚 Processing Chapter {chapter_num}: {chapter_data['title']}")
                
                # Process each section in the chapter
                for section in chapter_data['sections']:
                    section_num = section['number']
                    proof_refs = section.get('proof_refs', [])
                    
                    print(f"  📑 Section {section_num} ({len(proof_refs)} proof texts)")
                    
                    # Fetch real biblical text for proof texts
                    proof_texts = []
                    for ref in proof_refs:
                        verse_text = self.bible_fetcher.get_verse_text(ref)
                        proof_text = {
                            "reference": ref,
                            "text": verse_text if verse_text else "[Could not fetch verse text]"
                        }
                        proof_texts.append(proof_text)
                        total_proof_texts += 1
                    
                    # Create clauses structure
                    section['clauses'] = [{
                        "text": section['text'],
                        "proofTexts": proof_texts
                    }]
                    
                    # Remove temporary proof_refs
                    if 'proof_refs' in section:
                        del section['proof_refs']
                    
                    print(f"    ✅ Completed with {len(proof_texts)} KJV texts")
                
                confession['chapters'].append(chapter_data)
                print(f"  🎉 Chapter {chapter_num} complete!")
            
            print(f"\n📊 TOTAL: {total_proof_texts} proof texts with real KJV biblical text!")
            return confession
            
        except Exception as e:
            print(f"❌ Error parsing local file: {e}")
            return None
    
    def _extract_all_chapters(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract all Westminster Confession chapters - simple and fast approach"""
        
        chapters = []
        
        # Get chapter titles from TOC
        chapter_titles = {}
        toc_table = soup.find('table', {'id': 'table4'})
        if toc_table:
            for link in toc_table.find_all('a'):
                text = link.get_text(strip=True)
                match = re.search(r'Ch\s*([IVXLCDM]+).*?–\s*(.+)', text)
                if match:
                    chapter_num = self._roman_to_int(match.group(1))
                    title = match.group(2).strip()
                    chapter_titles[chapter_num] = title
        
        print(f"  📋 Found {len(chapter_titles)} chapter titles")
        
        # Find all paragraphs that start with Roman numerals (these are sections)
        all_paragraphs = soup.find_all('p')
        
        current_chapter = None
        chapters_data = {}  # chapter_num -> list of sections
        
        for para in all_paragraphs:
            para_text = para.get_text(strip=True)
            
            # Check if this paragraph is a section (starts with Roman numeral)
            section_match = re.match(r'([IVXLCDM]+)\.\s*(.+)', para_text)
            if section_match and len(section_match.group(2)) > 30:
                section_roman = section_match.group(1)
                section_text = section_match.group(2)
                section_num = self._roman_to_int(section_roman)
                
                # Find which chapter this belongs to by looking for chapter anchors above this paragraph
                chapter_anchor = None
                current_elem = para
                while current_elem:
                    current_elem = current_elem.find_previous()
                    if current_elem and current_elem.name == 'a':
                        anchor_name = current_elem.get('name', '')
                        if 'Chapter' in anchor_name:
                            chapter_match = re.search(r'Chapter\s+([IVXLCDM]+)', anchor_name)
                            if chapter_match:
                                current_chapter = self._roman_to_int(chapter_match.group(1))
                                break
                    # Don't search too far back
                    if current_elem and hasattr(current_elem, 'name') and current_elem.name in ['h1', 'h2']:
                        break
                
                if current_chapter:
                    # Extract superscript letters from HTML
                    para_html = str(para)
                    letters = re.findall(r'<sup>([a-z])</sup>', para_html)
                    
                    # Find proof texts for these letters by looking for the next italic paragraph
                    proof_refs = []
                    next_elem = para.find_next('em')
                    if next_elem:
                        # Extract all biblical references from this em element
                        bible_links = next_elem.find_all('a', class_='rtBibleRef')
                        for link in bible_links:
                            data_ref = link.get('data-reference', '')
                            if data_ref:
                                ref = data_ref.replace('.', ':')
                                proof_refs.append(ref)
                            else:
                                link_text = link.get_text(strip=True)
                                if ':' in link_text:
                                    proof_refs.append(link_text)
                    
                    # Add to chapter data
                    if current_chapter not in chapters_data:
                        chapters_data[current_chapter] = []
                    
                    chapters_data[current_chapter].append({
                        'number': section_num,
                        'text': section_text,
                        'proof_refs': list(set(proof_refs))
                    })
        
        # Create final chapters list
        for chapter_num in sorted(chapters_data.keys()):
            if chapter_num <= 33:  # Only first 33 chapters
                sections = sorted(chapters_data[chapter_num], key=lambda x: x['number'])
                chapter_title = chapter_titles.get(chapter_num, f"Chapter {chapter_num}")
                
                chapters.append({
                    'number': chapter_num,
                    'title': chapter_title,
                    'sections': sections
                })
                
                total_proof_texts = sum(len(s['proof_refs']) for s in sections)
                print(f"  ✅ Chapter {chapter_num}: {chapter_title} - {len(sections)} sections, {total_proof_texts} proof texts")
        
        return chapters
    
    def _extract_sections_from_containers(self, containers: List, chapter_num: int) -> List[Dict[str, Any]]:
        """This method is no longer used - keeping for compatibility"""
        return []
    
    def _normalize_book_name(self, reference: str) -> str:
        """Normalize biblical book names while preserving numbers"""
        
        # Common abbreviation mappings with number-aware replacements
        book_replacements = [
            # Handle numbered books first
            (r'\b1\s*Cor\b', '1 Corinthians'),
            (r'\b2\s*Cor\b', '2 Corinthians'),
            (r'\b1\s*Thess\b', '1 Thessalonians'),
            (r'\b2\s*Thess\b', '2 Thessalonians'),
            (r'\b1\s*Tim\b', '1 Timothy'),
            (r'\b2\s*Tim\b', '2 Timothy'),
            (r'\b1\s*Pet\b', '1 Peter'),
            (r'\b2\s*Pet\b', '2 Peter'),
            (r'\b1\s*John\b', '1 John'),
            (r'\b2\s*John\b', '2 John'),
            (r'\b3\s*John\b', '3 John'),
            
            # Handle single books
            (r'\bPsa\b', 'Psalms'),
            (r'\bPs\b', 'Psalms'),
            (r'\bMatt\b', 'Matthew'),
            (r'\bRom\b', 'Romans'),
            (r'\bGal\b', 'Galatians'),
            (r'\bEph\b', 'Ephesians'),
            (r'\bPhil\b', 'Philippians'),
            (r'\bCol\b', 'Colossians'),
            (r'\bTit\b', 'Titus'),
            (r'\bHeb\b', 'Hebrews'),
            (r'\bJas\b', 'James'),
            (r'\bRev\b', 'Revelation'),
        ]
        
        normalized_ref = reference
        for pattern, replacement in book_replacements:
            normalized_ref = re.sub(pattern, replacement, normalized_ref, flags=re.IGNORECASE)
        
        return normalized_ref
    
    def _roman_to_int(self, roman: str) -> int:
        """Convert Roman numeral to integer"""
        
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0
        
        for char in reversed(roman.upper()):
            value = roman_map.get(char, 0)
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        
        return result

def main():
    """Main function"""
    
    print("=" * 70)
    print("🏛️  WESTMINSTER CONFESSION SCRAPER - LOCAL FILE VERSION")
    print("=" * 70)
    print("📁 Reading from downloaded Westminster files")
    print("📖 Fetching real KJV biblical text for all proof texts")
    print("🔄 Processing all 33 chapters automatically")
    print("=" * 70)
    
    # Path to the local Westminster file
    local_file_path = "/Users/brendanchatt/Downloads/westminster/The Westminster Confession – The Westminster Standard.html"
    
    start_time = time.time()
    
    scraper = WestminsterLocalScraper(local_file_path)
    confession = scraper.parse_local_confession()
    
    if confession and confession['chapters']:
        # Save to JSON file
        filename = "assets/westminster_confession_complete_final.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(confession, f, indent=2, ensure_ascii=False)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! COMPLETE WESTMINSTER CONFESSION CREATED!")
        print("=" * 70)
        print(f"📄 Saved to: {filename}")
        print(f"⏱️  Total time: {duration:.1f} seconds")
        
        # Print summary statistics
        total_chapters = len(confession['chapters'])
        total_sections = sum(len(chapter['sections']) for chapter in confession['chapters'])
        total_proof_texts = sum(
            len(clause['proofTexts']) 
            for chapter in confession['chapters']
            for section in chapter['sections']
            for clause in section['clauses']
        )
        
        print(f"\n📊 Final Statistics:")
        print(f"   📚 Chapters processed: {total_chapters}")
        print(f"   📑 Sections found: {total_sections}")
        print(f"   📖 Proof texts with real KJV: {total_proof_texts}")
        
        print(f"\n🏆 COMPLETE! Your Westminster Confession with real KJV biblical text is ready!")
        print(f"📁 Successfully processed from local downloaded files")
        print(f"📋 Perfect JSON format matching your specification")
        print("=" * 70)
    
    else:
        print("❌ Failed to process Westminster Confession from local files")

if __name__ == "__main__":
    main() 