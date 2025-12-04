import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.content_generation_engine.pdf_qa_extractor import PDFQuestionExtractor

@pytest.fixture
def sample_pdf_path(tmp_path: Path) -> Path:
    """Creates a dummy PDF file for testing."""
    pdf_content = """
1 (a) Question text 1 (a) [2]
1 (b) Question text 1 (b) [5]
2. Question text 2 [3]
    """
    dummy_pdf = tmp_path / "sample.pdf"
    dummy_pdf.write_text(pdf_content)
    return dummy_pdf

@patch('pdfplumber.open')
def test_extract_questions_from_pdf(mock_pdfplumber_open, sample_pdf_path: Path):
    extractor = PDFQuestionExtractor()

    # Mock pdfplumber's behavior
    mock_pdf = MagicMock()
    mock_page = MagicMock()
    mock_page.extract_text.return_value = sample_pdf_path.read_text()
    mock_pdf.pages = [mock_page]
    mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

    questions = extractor.extract_questions_from_pdf(sample_pdf_path)

    assert len(questions) == 3

    assert questions[0]["question_number"] == "1(a)"
    assert "Question text 1 (a)" in questions[0]["question_text"]
    assert questions[0]["max_marks"] == 2

    assert questions[1]["question_number"] == "1(b)"
    assert "Question text 1 (b)" in questions[1]["question_text"]
    assert questions[1]["max_marks"] == 5

    assert questions[2]["question_number"] == "2"
    assert "Question text 2" in questions[2]["question_text"]
    assert questions[2]["max_marks"] == 3

    # Test with a PDF where no questions are found
    mock_page.extract_text.return_value = "This is a document with no questions."
    questions_none = extractor.extract_questions_from_pdf(sample_pdf_path)
    assert len(questions_none) == 0

    # Test with empty text
    mock_page.extract_text.return_value = ""
    questions_empty = extractor.extract_questions_from_pdf(sample_pdf_path)
    assert len(questions_empty) == 0