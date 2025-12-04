import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.core_database.database import Base
from src.core_database import crud, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.a_star_workflow_orchestrator.orchestrator import LearningLoop, run_full_loop

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

@patch('src.content_generation_engine.learning_pack_generator.generate_learning_pack')
@patch('src.content_generation_engine.exam_generator.generate_mock_exam')
def test_learning_loop(mock_generate_exam, mock_generate_lp, db_session: Session):
    # Setup: Create a student and some syllabus points
    student = crud.create_student(db_session, "orchestrator_student")
    sp1 = models.SyllabusPoint(subject="9706", code="1.1", description="The accounting cycle")
    db_session.add(sp1)
    db_session.commit()

    # Mock the content generation functions
    mock_lp = models.LearningPack(student_id=student.id, syllabus_points=[sp1])
    mock_exam = models.MockExam(student_id=student.id, subject="9706", questions=[
        models.Question(resource_id=1, question_number="1", max_marks=10)
    ])
    mock_generate_lp.return_value = mock_lp
    mock_generate_exam.return_value = mock_exam

    # Execute
    loop = LearningLoop(student_id=student.id, db=db_session, syllabus_topic_codes=["1.1"])
    assert loop.assign()
    assert loop.test()
    assert loop.diagnose()
    assert loop.remediate()
    assert loop.model()

    # Test the full loop runner
    run_full_loop(student_id=student.id, syllabus_topic_codes=["1.1"], db=db_session)
