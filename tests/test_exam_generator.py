import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.core_database.database import Base
from src.core_database import crud, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.content_generation_engine import exam_generator

# Setup in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine) # Create tables
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine) # Drop tables

def test_generate_mock_exam(db_session: Session):
    # Setup: Create a student and some questions
    student = crud.create_student(db_session, "exam_student")
    
    # Create a resource to associate with questions
    resource = models.Resource(subject="9706", year=2023, paper=1, variant=2, type="Past Paper", path="/path/to/exam_qp.pdf")
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)

    # Create questions linked to the resource
    q1 = models.Question(resource_id=resource.id, question_number="1", max_marks=10)
    q2 = models.Question(resource_id=resource.id, question_number="2", max_marks=15)
    q3 = models.Question(resource_id=resource.id, question_number="3", max_marks=5)
    db_session.add_all([q1, q2, q3])
    db_session.commit()
    
    # Execute
    mock_exam = exam_generator.generate_mock_exam(
        student_id=student.id,
        subject="9706",
        num_questions=2,
        db=db_session
    )
    
    # Verify
    assert mock_exam is not None
    assert mock_exam.student_id == student.id
    assert mock_exam.subject == "9706"
    assert len(mock_exam.questions) == 2

    # Test with insufficient questions
    not_enough_questions_exam = exam_generator.generate_mock_exam(
        student_id=student.id,
        subject="9706",
        num_questions=5, # Request more questions than available
        db=db_session
    )
    assert not_enough_questions_exam is None
