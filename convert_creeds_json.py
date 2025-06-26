#!/usr/bin/env python3
"""
Convert Creeds.json format to Westminster Standards format
"""

import json
import re
from typing import Dict, List, Any

def convert_confession(creeds_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Creeds.json confession format to Westminster Standards format"""
    
    # Extract metadata
    metadata = creeds_data.get("Metadata", {})
    
    result = {
        "title": metadata.get("Title", "The Westminster Confession of Faith"),
        "year": int(metadata.get("Year", "1647")),
        "chapters": []
    }
    
    # Process each chapter item
    for item in creeds_data.get("Data", []):
        chapter_num = item.get("Chapter", "1")
        sections = item.get("Sections", [])
        
        chapter = {
            "number": int(chapter_num),
            "title": f"Chapter {chapter_num}",
            "sections": []
        }
        
        for section in sections:
            section_num = section.get("Section", "1")
            content = section.get("Content", "")
            content_with_proofs = section.get("ContentWithProofs", content)
            proofs = section.get("Proofs", [])
            
            # Convert proofs to the expected format
            proof_texts = []
            for proof in proofs:
                references = proof.get("References", [])
                for ref in references:
                    # Convert reference format (e.g., "Ps.19.1-Ps.19.3" to "Ps 19:1-3")
                    formatted_ref = convert_reference_format(ref)
                    proof_texts.append({
                        "reference": formatted_ref,
                        "text": f"[{formatted_ref}]"  # Placeholder text
                    })
            
            # Create clauses (simplified - just one clause per section)
            clauses = [{
                "text": content,
                "proofTexts": proof_texts
            }]
            
            section_obj = {
                "number": int(section_num),
                "text": content,
                "clauses": clauses
            }
            
            chapter["sections"].append(section_obj)
        
        result["chapters"].append(chapter)
    
    return result

def convert_catechism(creeds_data: Dict[str, Any], is_larger: bool = False) -> Dict[str, Any]:
    """Convert Creeds.json catechism format to Westminster Standards format"""
    
    metadata = creeds_data.get("Metadata", {})
    
    result = {
        "title": metadata.get("Title", "Westminster Catechism"),
        "year": int(metadata.get("Year", "1647")),
        "questions": []
    }
    
    for item in creeds_data.get("Data", []):
        question_num = item.get("Number", 1)
        question_text = item.get("Question", "")
        answer_text = item.get("Answer", "")
        
        # Handle proofs for larger catechism
        proof_texts = []
        if is_larger:
            proofs = item.get("Proofs", [])
            for proof in proofs:
                references = proof.get("References", [])
                for ref in references:
                    formatted_ref = convert_reference_format(ref)
                    proof_texts.append({
                        "reference": formatted_ref,
                        "text": f"[{formatted_ref}]"  # Placeholder text
                    })
        
        qa_obj = {
            "number": question_num,
            "question": question_text,
            "answer": answer_text
        }
        
        if proof_texts:
            qa_obj["proofTexts"] = proof_texts
        
        result["questions"].append(qa_obj)
    
    return result

def convert_reference_format(ref: str) -> str:
    """Convert Creeds.json reference format to standard Bible reference format"""
    # Examples: "Ps.19.1-Ps.19.3" -> "Ps 19:1-3", "Rom.1.19-Rom.1.20" -> "Rom 1:19-20"
    
    # Handle ranges
    if "-" in ref:
        parts = ref.split("-")
        start_ref = parts[0]
        end_ref = parts[1]
        
        # Extract book and chapter from start
        start_match = re.match(r"([A-Za-z]+)\.(\d+)\.(\d+)", start_ref)
        end_match = re.match(r"([A-Za-z]+)\.(\d+)\.(\d+)", end_ref)
        
        if start_match and end_match:
            book = start_match.group(1)
            start_chapter = start_match.group(2)
            start_verse = start_match.group(3)
            end_verse = end_match.group(3)
            
            # Handle different books
            if start_chapter == end_match.group(2):  # Same chapter
                return f"{book} {start_chapter}:{start_verse}-{end_verse}"
            else:  # Different chapters
                end_chapter = end_match.group(2)
                return f"{book} {start_chapter}:{start_verse}-{end_chapter}:{end_verse}"
    
    # Handle single references
    match = re.match(r"([A-Za-z]+)\.(\d+)\.(\d+)", ref)
    if match:
        book = match.group(1)
        chapter = match.group(2)
        verse = match.group(3)
        return f"{book} {chapter}:{verse}"
    
    return ref

def main():
    """Main conversion function"""
    
    # Download and convert files
    import urllib.request
    
    files_to_convert = [
        {
            "url": "https://raw.githubusercontent.com/NonlinearFruit/Creeds.json/master/creeds/westminster_confession_of_faith.json",
            "output": "assets/westminster_confession.json",
            "type": "confession"
        },
        {
            "url": "https://raw.githubusercontent.com/NonlinearFruit/Creeds.json/master/creeds/westminster_shorter_catechism.json",
            "output": "assets/westminster_shorter_catechism.json",
            "type": "shorter_catechism"
        },
        {
            "url": "https://raw.githubusercontent.com/NonlinearFruit/Creeds.json/master/creeds/westminster_larger_catechism.json",
            "output": "assets/westminster_larger_catechism.json",
            "type": "larger_catechism"
        }
    ]
    
    for file_info in files_to_convert:
        print(f"Converting {file_info['type']}...")
        
        # Download the file
        with urllib.request.urlopen(file_info["url"]) as response:
            creeds_data = json.loads(response.read().decode())
        
        # Convert based on type
        if file_info["type"] == "confession":
            converted_data = convert_confession(creeds_data)
        elif file_info["type"] == "shorter_catechism":
            converted_data = convert_catechism(creeds_data, is_larger=False)
        elif file_info["type"] == "larger_catechism":
            converted_data = convert_catechism(creeds_data, is_larger=True)
        
        # Write the converted file
        with open(file_info["output"], "w", encoding="utf-8") as f:
            json.dump(converted_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Converted {file_info['type']} to {file_info['output']}")
    
    print("\nConversion complete! All files have been updated with data from Creeds.json")

if __name__ == "__main__":
    main() 