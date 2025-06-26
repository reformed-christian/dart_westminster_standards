#!/usr/bin/env python3
"""
Debug script to test Bible API URL construction
"""

import requests

def test_bible_api_urls():
    """Test various biblical references with the API"""
    
    base_url = "https://bible-api.com"
    translation = "kjv"
    
    test_references = [
        # Test both short and long forms
        "1 Cor 1:21",         # Short form
        "1 Corinthians 1:21", # Long form
        "2 Cor 13:14",        # Short form  
        "2 Corinthians 13:14", # Long form
        "1 Tim 3:15",         # Short form
        "1 Timothy 3:15",     # Long form
        "1 Pet 1:19",         # Short form
        "1 Peter 1:19",       # Long form
        "Romans 1:19",
        "Psalm 19:1"
    ]
    
    print("🧪 Testing Bible API URL Construction\n")
    
    for reference in test_references:
        # Convert reference for API (no normalization for testing)
        api_ref = reference.lower().replace(" ", "+")
        url = f"{base_url}/{api_ref}?translation={translation}"
        
        print(f"📖 Reference: {reference}")
        print(f"🔗 API URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'text' in data:
                    print(f"✅ Success: {data['text'][:50]}...")
                elif 'verses' in data and data['verses']:
                    print(f"✅ Success: {len(data['verses'])} verses found")
                else:
                    print(f"❓ Unexpected response format")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text[:100]}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    test_bible_api_urls() 