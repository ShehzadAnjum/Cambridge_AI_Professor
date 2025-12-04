import re
from pathlib import Path
from typing import Optional, Dict

class MetadataExtractor:
    """
    Handles the extraction of metadata from filenames and PDF content.
    """
    def __init__(self):
        """
        Initializes the MetadataExtractor with a regex pattern for filenames.
        """
        # Regex to extract metadata from filenames like "9706_s22_qp_12.pdf"
        self.filename_pattern = re.compile(
            r"^(?P<subject_code>\d{4})_"  # Subject code (e.g., 9706)
            r"(?P<season>[sw])(?P<year>\d{2})_"  # Season (s/w) and Year (e.g., s22)
            r"(?P<type>qp|ms|er)_"  # Type (qp=question paper, ms=mark scheme, er=examiner report)
            r"(?P<paper>\d{1,2})_"  # Paper number (e.g., 1, 2, 3)
            r"(?P<variant>\d{1,2})"  # Variant (e.g., 1, 2)
            r"\.pdf$"  # .pdf extension
        )

    def extract_metadata_from_filename(self, filepath: Path) -> Optional[Dict[str, str]]:
        """
        Extracts metadata from a given filename based on predefined patterns.

        Args:
            filepath: The path to the file.

        Returns:
            A dictionary containing extracted metadata (subject_code, season, year, type, paper, variant)
            or None if the filename does not match the pattern.
        """
        match = self.filename_pattern.match(filepath.name)
        if match:
            metadata = match.groupdict()
            # Map short codes to full types
            type_map = {
                "qp": "Past Paper",
                "ms": "Mark Scheme",
                "er": "Examiner Report"
            }
            metadata['type'] = type_map.get(metadata['type'], metadata['type'])
            # Convert year to full format (e.g., 22 -> 2022)
            metadata['year'] = f"20{metadata['year']}"
            return metadata
        return None

    def extract_text_from_pdf(self, filepath: Path) -> Optional[str]:
        """
        Extracts text content from a PDF file using pdfminer.six.

        Args:
            filepath: The path to the PDF file.

        Returns:
            The extracted text content as a string, or None if an error occurs.
        """
        try:
            from pdfminer.high_level import extract_text
            return extract_text(str(filepath))
        except Exception as e:
            print(f"Error extracting text from {filepath}: {e}")
            return None

    def get_metadata_from_pdf_content(self, filepath: Path) -> Optional[Dict[str, str]]:
        """
        Extracts metadata from the content of a PDF file.
        (Placeholder for more advanced extraction logic)

        Args:
            filepath: The path to the PDF file.

        Returns:
            A dictionary containing extracted metadata or None.
        """
        text_content = self.extract_text_from_pdf(filepath)
        if text_content:
            # Implement logic to parse text content for metadata, e.g., syllabus code
            # For now, this is a placeholder.
            return {"content_metadata": "extracted_from_content"}
        return None
