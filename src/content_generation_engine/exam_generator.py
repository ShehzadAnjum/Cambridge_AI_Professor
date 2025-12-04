from typing import List, Optional
from sqlalchemy.orm import Session
from src.core_database import crud, models
from src.content_generation_engine.pdf_qa_extractor import PDFQuestionExtractor
import random
import sys

def generate_mock_exam(
    student_id: int,
    subject: str,
    num_questions: int,
    db: Session
) -> Optional[models.MockExam]:
    """
    Generates a mock exam for a given student and subject.

    Args:
        student_id: The ID of the student.
        subject: The subject code (e.g., "9706") for the exam.
        num_questions: The number of questions to include in the exam.
        db: The database session.

    Returns:
        The newly created MockExam object, or None if insufficient questions are available.
    """
    try:
        # 1. Find all available questions for the subject
        # This assumes questions have been extracted and stored in the 'questions' table.
        # We will need a way to populate this table first.
        # For now, let's assume the 'questions' table is populated by a separate process
        # using pdf_qa_extractor.py.
        
        all_questions = db.query(models.Question).filter(
            models.Resource.subject == subject # Need to join with Resource to filter by subject
        ).join(models.Resource).all()

        if len(all_questions) < num_questions:
            print(f"Insufficient questions available for subject {subject} to create an exam of {num_questions} questions.", file=sys.stderr)
            return None

        # 2. Select a random sample of questions
        selected_questions = random.sample(all_questions, num_questions)

        # 3. Create the mock exam
        mock_exam = crud.create_mock_exam(
            db=db,
            student_id=student_id,
            subject=subject,
            question_ids=[q.id for q in selected_questions]
        )

        return mock_exam
    except Exception as e:
        print(f"Error generating mock exam: {e}", file=sys.stderr)
        return None
