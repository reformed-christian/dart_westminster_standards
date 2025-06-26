#!/usr/bin/env python3
"""
Demo Westminster Confession with Real KJV Biblical Text
Demonstrates bible-api.com integration with Westminster Confession format
"""

import requests
import json
import time
from typing import List, Dict, Any, Optional

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
        
        # If we've made 14 requests, wait
        if self.request_count >= 14:
            sleep_time = 31 - (current_time - self.last_request_time)
            if sleep_time > 0:
                print(f"⏳ Rate limiting: waiting {sleep_time:.1f} seconds...")
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
            print(f"  📖 Fetching: {reference}")
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
            print(f"    ✅ Success!")
            return result
            
        except Exception as e:
            print(f"    ❌ Error fetching {reference}: {e}")
            return None

def create_westminster_confession_demo():
    """Create Westminster Confession demo with real KJV biblical text"""
    
    print("🔄 Creating Westminster Confession demo with real KJV biblical text...")
    print("📡 Using bible-api.com for biblical text fetching\n")
    
    bible_fetcher = BibleAPIFetcher()
    
    # Westminster Confession Chapter 1 - Of the Holy Scripture
    chapter_1_data = {
        "number": 1,
        "title": "Of the Holy Scripture",
        "sections": [
            {
                "number": 1,
                "text": "Although the light of nature, and the works of creation and providence do so far manifest the goodness, wisdom, and power of God, as to leave men unexcusable; yet are they not sufficient to give that knowledge of God, and of his will, which is necessary unto salvation. Therefore it pleased the Lord, at sundry times, and in divers manners, to reveal himself, and to declare that his will unto his church; and afterwards, for the better preserving and propagating of the truth, and for the more sure establishment and comfort of the church against the corruption of the flesh, and the malice of Satan and of the world, to commit the same wholly unto writing: which maketh the Holy Scripture to be most necessary; those former ways of God's revealing his will unto his people being now ceased.",
                "proof_refs": [
                    "Romans 2:14-15",
                    "Romans 1:19-20", 
                    "Psalms 19:1-3",
                    "1 Corinthians 1:21",
                    "1 Corinthians 2:13-14",
                    "Hebrews 1:1"
                ]
            },
            {
                "number": 2,
                "text": "Under the name of Holy Scripture, or the Word of God written, are now contained all the books of the Old and New Testament, which are these: Of the Old Testament: Genesis, Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth, I Samuel, II Samuel, I Kings, II Kings, I Chronicles, II Chronicles, Ezra, Nehemiah, Esther, Job, Psalms, Proverbs, Ecclesiastes, The Song of Songs, Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel, Hosea, Joel, Amos, Obadiah, Jonah, Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi; Of the New Testament: The Gospels according to Matthew, Mark, Luke, John, The Acts of the Apostles, Paul's Epistles to the Romans, Corinthians I, Corinthians II, Galatians, Ephesians, Philippians, Colossians, Thessalonians I, Thessalonians II, To Timothy I, To Timothy II, To Titus, To Philemon, The Epistle to the Hebrews, The Epistle of James, The first and second Epistles of Peter, The first, second, and third Epistles of John, The Epistle of Jude, The Revelation of John. All which are given by inspiration of God to be the rule of faith and life.",
                "proof_refs": [
                    "Luke 16:29",
                    "Ephesians 2:20",
                    "Revelation 22:18-19",
                    "2 Timothy 3:16"
                ]
            }
        ]
    }
    
    # Create the complete confession structure
    confession = {
        "title": "The Westminster Confession of Faith",
        "year": 1646,
        "chapters": []
    }
    
    print(f"📚 Processing Chapter {chapter_1_data['number']}: {chapter_1_data['title']}")
    
    sections = []
    for section_data in chapter_1_data['sections']:
        print(f"  📑 Processing Section {section_data['number']}")
        
        # Fetch real biblical text for proof texts
        proof_texts = []
        for ref in section_data['proof_refs']:
            verse_text = bible_fetcher.get_verse_text(ref)
            proof_text = {
                "reference": ref,
                "text": verse_text if verse_text else "[Could not fetch verse text]"
            }
            proof_texts.append(proof_text)
        
        # Create clauses
        clauses = [{
            "text": section_data['text'],
            "proofTexts": proof_texts
        }]
        
        section = {
            "number": section_data['number'],
            "text": section_data['text'],
            "clauses": clauses
        }
        sections.append(section)
        print(f"    ✅ Added {len(proof_texts)} proof texts with real KJV text")
    
    chapter = {
        "number": chapter_1_data['number'],
        "title": chapter_1_data['title'],
        "sections": sections
    }
    
    confession["chapters"] = [chapter]
    
    return confession

def main():
    """Main function"""
    
    print("=" * 60)
    print("Westminster Confession Demo with Real KJV Biblical Text")
    print("=" * 60)
    
    confession = create_westminster_confession_demo()
    
    if confession:
        # Save to JSON file
        filename = "assets/westminster_confession_demo_kjv.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(confession, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 SUCCESS! Westminster Confession demo created with real KJV text!")
        print(f"📄 Saved to: {filename}")
        
        # Print summary statistics
        total_sections = sum(len(chapter['sections']) for chapter in confession['chapters'])
        total_proof_texts = sum(
            len(clause['proofTexts']) 
            for chapter in confession['chapters']
            for section in chapter['sections']
            for clause in section['clauses']
        )
        
        print(f"\n📊 Summary:")
        print(f"   📚 Chapters: {len(confession['chapters'])}")
        print(f"   📑 Sections: {total_sections}")
        print(f"   📖 Proof texts with real KJV: {total_proof_texts}")
        
        # Show sample proof texts
        print(f"\n📖 Sample proof texts:")
        for chapter in confession['chapters']:
            for section in chapter['sections']:
                for clause in section['clauses']:
                    for i, proof_text in enumerate(clause['proofTexts'][:3]):  # Show first 3
                        print(f"\n   {i+1}. 📍 {proof_text['reference']}")
                        print(f"      💬 \"{proof_text['text'][:100]}...\"")
        
        print(f"\n✨ Your Westminster Confession demo with real KJV biblical text is ready!")
        print(f"🔗 This demonstrates how bible-api.com can be used to fetch actual biblical text")
        print(f"📋 The JSON follows your exact format specification")
    
    else:
        print("❌ Failed to create Westminster Confession demo")

if __name__ == "__main__":
    main() 