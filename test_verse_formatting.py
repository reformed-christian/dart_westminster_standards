#!/usr/bin/env python3
"""
Test script to demonstrate corrected verse formatting
"""

import requests
import json
import time
import re
from typing import Optional

class BibleAPIFetcher:
    """Test version of Bible fetcher with corrected formatting"""
    
    def __init__(self):
        self.base_url = "https://bible-api.com"
        self.translation = "kjv"
        
    def _is_consecutive_range(self, reference: str) -> bool:
        """Check if reference is a consecutive range like 'Romans 1:19-20' vs comma-separated like 'Matthew 5:11, 17'"""
        return '-' in reference and ',' not in reference
    
    def get_verse_text(self, reference: str) -> Optional[str]:
        """Get verse text with proper formatting"""
        
        # Convert reference for API
        api_ref = reference.lower().replace(" ", "+").replace("psalm", "psalms")
        url = f"{self.base_url}/{api_ref}?translation={self.translation}"
        
        try:
            print(f"📖 Testing: {reference}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'verses' in data and data['verses']:
                verse_texts = []
                is_consecutive = self._is_consecutive_range(reference)
                
                print(f"   Type: {'Consecutive range' if is_consecutive else 'Comma-separated or single'}")
                
                for verse in data['verses']:
                    verse_num = verse.get('verse', '')
                    verse_text = verse.get('text', '').strip()
                    
                    if is_consecutive:
                        # For consecutive ranges, include verse numbers in brackets
                        verse_texts.append(f"[{verse_num}] {verse_text}")
                    else:
                        # For comma-separated verses
                        if len(data['verses']) > 1:
                            verse_texts.append(f"[{verse_num}] {verse_text}")
                        else:
                            verse_texts.append(verse_text)
                
                # Join appropriately
                if is_consecutive:
                    # For consecutive verses, join directly without pipe - they flow together
                    result = " ".join(verse_texts)
                else:
                    # For comma-separated verses, use " | " to separate distinct citations
                    result = " | ".join(verse_texts)
                    
            else:
                result = data.get('text', '').strip()
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def main():
    """Test the formatting"""
    
    print("🧪 Testing Verse Formatting Correction\n")
    
    fetcher = BibleAPIFetcher()
    
    # Test cases
    test_cases = [
        "Romans 1:19-20",  # Consecutive - should NOT use pipe
        "Romans 1:19",     # Single verse
        "Psalms 19:1-3",   # Consecutive - should NOT use pipe
    ]
    
    for reference in test_cases:
        result = fetcher.get_verse_text(reference)
        print(f"   Result: {result[:100]}...")
        print(f"   Uses pipe: {'|' in result}")
        print()
        time.sleep(2.5)  # Rate limiting

if __name__ == "__main__":
    main() 