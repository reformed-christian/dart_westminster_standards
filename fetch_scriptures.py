#!/usr/bin/env python3
"""
Script to fetch actual scripture text from KJV JSON file
"""

import json
import re
from typing import Dict, List, Optional, Tuple

class ScriptureFetcher:
    def __init__(self, kjv_file_path: str = "kjv.json"):
        """Initialize with KJV JSON file path"""
        self.kjv_file_path = kjv_file_path
        self.verses = {}
        self.book_names = {}
        self._load_kjv_data()
        self._setup_book_mapping()
    
    def _load_kjv_data(self):
        """Load KJV data from JSON file"""
        print("Loading KJV data...")
        with open(self.kjv_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract verses from the structure
        rows = data.get("resultset", {}).get("row", [])
        
        for row in rows:
            field = row.get("field", [])
            if len(field) >= 5:
                verse_id, book_num, chapter, verse, text = field
                key = f"{book_num:02d}{chapter:03d}{verse:03d}"
                self.verses[key] = {
                    "book": book_num,
                    "chapter": chapter,
                    "verse": verse,
                    "text": text
                }
        
        print(f"Loaded {len(self.verses)} verses")
    
    def _setup_book_mapping(self):
        """Setup mapping from book names to book numbers"""
        self.book_names = {
            # Old Testament
            "gen": 1, "genesis": 1,
            "exo": 2, "exod": 2, "exodus": 2,
            "lev": 3, "leviticus": 3,
            "num": 4, "numbers": 4,
            "deu": 5, "deut": 5, "deuteronomy": 5,
            "jos": 6, "josh": 6, "joshua": 6,
            "jud": 7, "judg": 7, "judges": 7,
            "rut": 8, "ruth": 8,
            "1sa": 9, "1sam": 9, "1samuel": 9, "i samuel": 9, "1 samuel": 9,
            "2sa": 10, "2sam": 10, "2samuel": 10, "ii samuel": 10, "2 samuel": 10,
            "1ki": 11, "1kgs": 11, "1kings": 11, "i kings": 11, "1 kings": 11,
            "2ki": 12, "2kgs": 12, "2kings": 12, "ii kings": 12, "2 kings": 12,
            "1ch": 13, "1chr": 13, "1chron": 13, "1chronicles": 13, "i chronicles": 13, "1 chronicles": 13,
            "2ch": 14, "2chr": 14, "2chron": 14, "2chronicles": 14, "ii chronicles": 14, "2 chronicles": 14,
            "ezr": 15, "ezra": 15,
            "neh": 16, "nehemiah": 16,
            "est": 17, "esth": 17, "esther": 17,
            "job": 18,
            "psa": 19, "ps": 19, "psalm": 19, "psalms": 19,
            "pro": 20, "prov": 20, "proverbs": 20,
            "ecc": 21, "eccl": 21, "ecclesiastes": 21,
            "son": 22, "song": 22, "songs": 22, "songofsolomon": 22, "song of solomon": 22,
            "isa": 23, "isaiah": 23,
            "jer": 24, "jeremiah": 24,
            "lam": 25, "lamentations": 25,
            "eze": 26, "ezek": 26, "ezekiel": 26,
            "dan": 27, "daniel": 27,
            "hos": 28, "hosea": 28,
            "joe": 29, "joel": 29,
            "amo": 30, "amos": 30,
            "oba": 31, "obad": 31, "obadiah": 31,
            "jon": 32, "jonah": 32,
            "mic": 33, "micah": 33,
            "nah": 34, "nahum": 34,
            "hab": 35, "habakkuk": 35,
            "zep": 36, "zeph": 36, "zephaniah": 36,
            "hag": 37, "haggai": 37,
            "zac": 38, "zech": 38, "zechariah": 38,
            "mal": 39, "malachi": 39,
            
            # New Testament
            "mat": 40, "matt": 40, "matthew": 40,
            "mar": 41, "mark": 41,
            "luk": 42, "luke": 42,
            "joh": 43, "john": 43,
            "act": 44, "acts": 44,
            "rom": 45, "romans": 45,
            "1co": 46, "1cor": 46, "1corinthians": 46, "i corinthians": 46, "1 corinthians": 46,
            "2co": 47, "2cor": 47, "2corinthians": 47, "ii corinthians": 47, "2 corinthians": 47,
            "gal": 48, "galatians": 48,
            "eph": 49, "ephesians": 49,
            "phi": 50, "phil": 50, "philippians": 50,
            "col": 51, "colossians": 51,
            "1th": 52, "1thess": 52, "1thessalonians": 52, "i thessalonians": 52, "1 thessalonians": 52,
            "2th": 53, "2thess": 53, "2thessalonians": 53, "ii thessalonians": 53, "2 thessalonians": 53,
            "1ti": 54, "1tim": 54, "1timothy": 54, "i timothy": 54, "1 timothy": 54,
            "2ti": 55, "2tim": 55, "2timothy": 55, "ii timothy": 55, "2 timothy": 55,
            "tit": 56, "titus": 56,
            "phm": 57, "philem": 57, "philemon": 57,
            "heb": 58, "hebrews": 58,
            "jam": 59, "jas": 59, "james": 59,
            "1pe": 60, "1pet": 60, "1peter": 60, "i peter": 60, "1 peter": 60,
            "2pe": 61, "2pet": 61, "2peter": 61, "ii peter": 61, "2 peter": 61,
            "1jo": 62, "1john": 62, "i john": 62, "1 john": 62,
            "2jo": 63, "2john": 63, "ii john": 63, "2 john": 63,
            "3jo": 64, "3john": 64, "iii john": 64, "3 john": 64,
            "jud": 65, "jude": 65,
            "rev": 66, "revelation": 66
        }
    
    def parse_reference(self, reference: str):
        """Parse a Bible reference like 'Ps 19:1', 'Rom 1:19-20', 'Ps.51', 'Job.38-Job.41', etc."""
        # First, convert dot notation to colon notation for book.chapter.verse format
        # Pattern: BookName.Chapter.Verse -> BookName Chapter:Verse (use global replacement)
        ref = re.sub(r'([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)', r'\1 \2:\3', reference)
        
        # Then normalize: remove remaining periods, extra spaces, and lowercase
        ref = ref.replace('.', '').replace('  ', ' ').strip().lower()
        
        # Handle comma-separated references (return a list of parsed refs)
        if ',' in ref:
            refs = [r.strip() for r in ref.split(',') if r.strip()]
            return [self.parse_reference(r) for r in refs]
        
        # Handle chapter range: e.g., job38-job41
        chapter_range_match = re.match(r'([1-3]?[a-z]+)\s*(\d+)-(?:[1-3]?[a-z]+)?\s*(\d+)$', ref)
        if chapter_range_match:
            book_name = chapter_range_match.group(1)
            start_chapter = int(chapter_range_match.group(2))
            end_chapter = int(chapter_range_match.group(3))
            book_num = self.book_names.get(book_name)
            if book_num:
                return (book_num, start_chapter, 1, end_chapter, 'chapter_range')
        
        # Handle chapter only: e.g., ps51
        chapter_only_match = re.match(r'([1-3]?[a-z]+)\s*(\d+)$', ref)
        if chapter_only_match:
            book_name = chapter_only_match.group(1)
            chapter = int(chapter_only_match.group(2))
            book_num = self.book_names.get(book_name)
            if book_num:
                return (book_num, chapter, 1, chapter, 'chapter_only')
        
        # Handle range references like "rom 1:19-20" or "1cor 2:9-12"
        if '-' in ref:
            parts = ref.split('-')
            if len(parts) == 2:
                start_ref = parts[0].strip()
                end_part = parts[1].strip()
                
                # Parse start reference
                start_match = re.match(r'([1-3]?[a-z]+)\s*(\d+):(\d+)', start_ref)
                if start_match:
                    book_name = start_match.group(1)
                    chapter = int(start_match.group(2))
                    start_verse = int(start_match.group(3))
                    book_num = self.book_names.get(book_name)
                    
                    # Handle end part - could be just verse number, chapter:verse, or full book chapter:verse
                    if ':' in end_part:
                        # Check if it's a full reference like "1cor 10:4"
                        full_end_match = re.match(r'([1-3]?[a-z]+)\s*(\d+):(\d+)', end_part)
                        if full_end_match:
                            end_book_name = full_end_match.group(1)
                            end_chapter = int(full_end_match.group(2))
                            end_verse = int(full_end_match.group(3))
                            
                            # Check if it's the same book
                            if book_name == end_book_name:
                                if chapter == end_chapter:
                                    # Same chapter range
                                    if book_num:
                                        return (book_num, chapter, start_verse, end_verse, 'verse_range')
                                else:
                                    # Cross-chapter range
                                    if book_num:
                                        return (book_num, chapter, start_verse, end_chapter, end_verse, 'cross_chapter_range')
                            else:
                                # Different books - not supported
                                return None
                        else:
                            # Just chapter:verse format like "10:4"
                            end_match = re.match(r'(\d+):(\d+)', end_part)
                            if end_match:
                                end_chapter = int(end_match.group(1))
                                end_verse = int(end_match.group(2))
                                if chapter != end_chapter:
                                    if book_num:
                                        return (book_num, chapter, start_verse, end_chapter, end_verse, 'cross_chapter_range')
                                    else:
                                        return None
                                else:
                                    end_verse = int(end_match.group(2))
                                    if book_num:
                                        return (book_num, chapter, start_verse, end_verse, 'verse_range')
                            else:
                                return None
                    else:
                        # Just verse number like "4"
                        try:
                            end_verse = int(end_part)
                            if book_num:
                                return (book_num, chapter, start_verse, end_verse, 'verse_range')
                        except ValueError:
                            return None
        
        # Handle single verse references like "ps 19:1"
        match = re.match(r'([1-3]?[a-z]+)\s*(\d+):(\d+)', ref)
        if match:
            book_name = match.group(1)
            chapter = int(match.group(2))
            verse = int(match.group(3))
            book_num = self.book_names.get(book_name)
            if book_num:
                return (book_num, chapter, verse, verse, 'single_verse')
        
        return None
    
    def get_verse_text(self, book_num: int, chapter: int, verse: int) -> Optional[str]:
        key = f"{book_num:02d}{chapter:03d}{verse:03d}"
        verse_data = self.verses.get(key)
        return verse_data.get("text") if verse_data else None
    
    def get_verses_text(self, reference: str) -> Optional[str]:
        parsed = self.parse_reference(reference)
        if not parsed:
            print(f"[WARN] Could not parse reference: {reference}")
            return f"[{reference}]"
        # Handle comma-separated references (list of parsed refs)
        if isinstance(parsed, list):
            texts = [self.get_verses_text_from_parsed(p) for p in parsed if p]
            return " ".join([t for t in texts if t])
        return self.get_verses_text_from_parsed(parsed)

    def get_verses_text_from_parsed(self, parsed) -> Optional[str]:
        if not parsed:
            return None
        if parsed[-1] == 'single_verse':
            book_num, chapter, verse, _, _ = parsed
            text = self.get_verse_text(book_num, chapter, verse)
            return f"[{verse}] {text}" if text else None
        elif parsed[-1] == 'verse_range':
            book_num, chapter, start_verse, end_verse, _ = parsed
            verses = []
            for verse_num in range(start_verse, end_verse + 1):
                text = self.get_verse_text(book_num, chapter, verse_num)
                if text:
                    verses.append(f"[{verse_num}] {text}")
            return " ".join(verses) if verses else None
        elif parsed[-1] == 'chapter_only':
            book_num, chapter, _, _, _ = parsed
            verses = []
            for verse_num in range(1, 200):  # Arbitrary upper bound
                text = self.get_verse_text(book_num, chapter, verse_num)
                if not text:
                    break
                verses.append(f"[{verse_num}] {text}")
            return " ".join(verses) if verses else None
        elif parsed[-1] == 'chapter_range':
            book_num, start_chapter, _, end_chapter, _ = parsed
            verses = []
            for chapter in range(start_chapter, end_chapter + 1):
                for verse_num in range(1, 200):
                    text = self.get_verse_text(book_num, chapter, verse_num)
                    if not text:
                        break
                    verses.append(f"[{chapter}:{verse_num}] {text}")
            return " ".join(verses) if verses else None
        elif parsed[-1] == 'cross_chapter_range':
            # Not implemented: cross-chapter verse ranges
            print(f"[WARN] Cross-chapter verse range not supported: {parsed}")
            return None
        else:
            print(f"[WARN] Unknown parse type for reference: {parsed}")
            return None
    
    def update_proof_texts(self, proof_texts: List[Dict]) -> List[Dict]:
        """Update proof texts with actual scripture text"""
        updated_proof_texts = []
        
        for proof in proof_texts:
            reference = proof.get("reference", "")
            text = self.get_verses_text(reference)
            
            updated_proof = {
                "reference": reference,
                "text": text if text else f"[{reference}]"
            }
            updated_proof_texts.append(updated_proof)
        
        return updated_proof_texts

def main():
    """Test the scripture fetcher"""
    fetcher = ScriptureFetcher()
    
    # Test some references
    test_references = [
        "Ps 19:1-3",
        "Rom 1:19-20", 
        "John 3:16",
        "Gen 1:1",
        "Matt 4:4"
    ]
    
    print("\nTesting scripture fetcher:")
    print("=" * 50)
    
    for ref in test_references:
        text = fetcher.get_verses_text(ref)
        print(f"{ref}: {text}")
        print("-" * 30)

if __name__ == "__main__":
    main() 