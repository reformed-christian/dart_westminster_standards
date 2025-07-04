import fitz
import re

PDF_PATH = "sources/Larger_Catechism-prts.pdf"

def analyze_page_structure():
    doc = fitz.open(PDF_PATH)
    
    # Analyze pages 3-41 (content pages)
    for page_num in range(2, 41):  # 0-indexed, so pages 3-41
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        print(f"\n=== PAGE {page_num + 1} ===")
        
        # Look for standalone numbers that might be page numbers
        standalone_numbers = []
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        font_flags = span.get('flags', 0)
                        font_size = span.get('size', 0)
                        font_name = span.get('font', '')
                        
                        # Check if this is a standalone number
                        if text.isdigit() and len(text) <= 3:
                            standalone_numbers.append({
                                'text': text,
                                'font_size': font_size,
                                'font_name': font_name,
                                'flags': font_flags,
                                'line_text': ' '.join([s.get('text', '') for s in line.get('spans', [])])
                            })
        
        # Print standalone numbers found
        if standalone_numbers:
            print(f"Standalone numbers found: {len(standalone_numbers)}")
            for num in standalone_numbers[:5]:  # Show first 5
                print(f"  Number: {num['text']}, Font: {num['font_name']} ({num['font_size']:.1f}pt), Line: '{num['line_text']}'")
            if len(standalone_numbers) > 5:
                print(f"  ... and {len(standalone_numbers) - 5} more")

def analyze_font_patterns():
    """Analyze font patterns to distinguish page numbers from footnote numbers"""
    doc = fitz.open(PDF_PATH)
    
    # Collect all standalone numbers and their properties
    all_numbers = []
    
    for page_num in range(2, 41):
        page = doc[page_num]
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if block.get('type') == 0:
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()
                        
                        if text.isdigit() and len(text) <= 3:
                            font_flags = span.get('flags', 0)
                            font_size = span.get('size', 0)
                            font_name = span.get('font', '')
                            
                            all_numbers.append({
                                'number': int(text),
                                'font_size': font_size,
                                'font_name': font_name,
                                'flags': font_flags,
                                'page': page_num + 1
                            })
    
    # Analyze patterns
    print("=== FONT PATTERN ANALYSIS ===")
    
    # Group by font properties
    font_groups = {}
    for num in all_numbers:
        key = (num['font_name'], round(num['font_size'], 1))
        if key not in font_groups:
            font_groups[key] = []
        font_groups[key].append(num)
    
    for (font_name, font_size), numbers in font_groups.items():
        print(f"\nFont: {font_name} ({font_size}pt) - {len(numbers)} numbers")
        print(f"  Number range: {min(n['number'] for n in numbers)} - {max(n['number'] for n in numbers)}")
        print(f"  Sample numbers: {[n['number'] for n in numbers[:10]]}")
        
        # Check if this looks like page numbers (should be sequential)
        sorted_numbers = sorted([n['number'] for n in numbers])
        if len(sorted_numbers) > 1:
            gaps = [sorted_numbers[i+1] - sorted_numbers[i] for i in range(len(sorted_numbers)-1)]
            avg_gap = sum(gaps) / len(gaps)
            print(f"  Average gap: {avg_gap:.1f}")

if __name__ == "__main__":
    print("Analyzing PDF structure...")
    analyze_page_structure()
    analyze_font_patterns() 