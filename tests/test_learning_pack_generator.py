import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.core_database.database import Base
from src.core_database import crud, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.content_generation_engine import learning_pack_generator

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

def test_generate_learning_pack(db_session: Session):
    # Setup: Create a student, syllabus points, and resources
    student = crud.create_student(db_session, "test_student")
    
    sp1 = models.SyllabusPoint(subject="9706", code="1.1", description="The accounting cycle")
    sp2 = models.SyllabusPoint(subject="9706", code="1.2", description="Source documents")
    db_session.add_all([sp1, sp2])
    db_session.commit()

    resource1 = models.Resource(subject="9706", year=2022, paper=1, variant=2, type="Past Paper", path="/path/to/qp.pdf")
    resource2 = models.Resource(subject="9706", year=2022, paper=1, variant=2, type="Mark Scheme", path="/path/to/ms.pdf")
    db_session.add_all([resource1, resource2])
    db_session.commit()
    
    # Execute
    learning_pack = learning_pack_generator.generate_learning_pack(
        student_id=student.id,
        syllabus_topic_codes=["1.1", "1.2"],
        db=db_session
    )
    
    # Verify
    assert learning_pack is not None
    assert learning_pack.student_id == student.id
    assert len(learning_pack.syllabus_points) == 2
    assert len(learning_pack.resources) == 2 # Based on the placeholder logic

    # Test with no syllabus points found
    no_pack = learning_pack_generator.generate_learning_pack(
        student_id=student.id,
        syllabus_topic_codes=["99.9"],
        db=db_session
    )
    assert no_pack is None

    # Test with no resources found
    db_session.query(models.Resource).delete() # Remove resources
    db_session.commit()
    no_resources_pack = learning_pack_generator.generate_learning_pack(
        student_id=student.id,
        syllabus_topic_codes=["1.1"],
        db=db_session
    )
    assert no_resources_pack is None
