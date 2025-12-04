from pathlib import Path
from typing import List, Dict, Any, Optional
import pdfplumber
import re

class PDFQuestionExtractor:
    """
    Extracts questions and their maximum marks from PDF past papers.
    """
    def __init__(self) -> None:
        """
        Initializes the PDFQuestionExtractor with regex patterns for question numbers.
        """
        # This pattern identifies the start of a new question number,
        # e.g., "1", "1 (a)", "2." at the beginning of a line.
        # It captures the main number and optionally the part (a), (b)
        self.question_number_pattern = re.compile(r"^\s*(\d+)\s*(\([a-z]\))?\.?", re.MULTILINE | re.IGNORECASE)
        # We will use string manipulation for marks, not regex

    def extract_questions_from_pdf(self, filepath: Path) -> List[Dict[str, Any]]:
        """
        Extracts questions and their maximum marks from a PDF file.

        Args:
            filepath: The path to the PDF file.

        Returns:
            A list of dictionaries, each representing a question with its text and max_marks.
        """
        questions: List[Dict[str, Any]] = []
        try:
            with pdfplumber.open(filepath) as pdf:
                full_text = ""
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        full_text += extracted_text + "\n"
                
                # Find all start positions of new questions
                question_starts_matches = list(self.question_number_pattern.finditer(full_text))
                
                if not question_starts_matches:
                    return []

                # Group text into question blocks
                for i, match_obj in enumerate(question_starts_matches):
                    start_pos = match_obj.start()
                    end_pos = question_starts_matches[i+1].start() if i+1 < len(question_starts_matches) else len(full_text)
                    
                    question_block = full_text[start_pos:end_pos].strip()

                    if not question_block:
                        continue

                    # Re-match the question number to extract it cleanly from the block
                    qn_num_match = self.question_number_pattern.match(question_block)
                    if not qn_num_match:
                        continue # Should not happen if logic is correct

                    qn_main = qn_num_match.group(1)
                    qn_part = qn_num_match.group(2) if qn_num_match.group(2) else ""
                    question_num_full = qn_main + qn_part
                    
                    # The text part of the question is everything after the question number prefix
                    question_text_raw = question_block[qn_num_match.end():].strip()

                    # Extract marks with string manipulation
                    max_marks = None
                    clean_question_text = question_text_raw
                    if "[" in question_text_raw and "]" in question_text_raw:
                        start = question_text_raw.rfind('[')
                        end = question_text_raw.rfind(']')
                        if start < end:
                            marks_str = question_text_raw[start+1:end].strip()
                            # Find the number inside the marks string
                            marks_num_match = re.search(r'\d+', marks_str)
                            if marks_num_match:
                                max_marks = int(marks_num_match.group(0))
                            # Clean the text
                            clean_question_text = question_text_raw[:start].strip()

                    questions.append({
                        "question_number": question_num_full,
                        "question_text": clean_question_text,
                        "max_marks": max_marks
                    })

        except Exception as e:
            print(f"Error extracting questions from {filepath}: {e}")
        return questions
