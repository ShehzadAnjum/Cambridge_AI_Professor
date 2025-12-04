import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core_database.database import Base
from src.core_database import crud, models

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session for each test function.
    Rollback changes after each test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_and_get_resource(db_session):
    """
    Test creating a new resource and retrieving it from the database.
    """
    from sqlalchemy.orm import Session

    resource_data = {
        "subject": "Mathematics",
        "year": 2022,
        "paper": 1,
        "variant": 2,
        "type": "Past Paper",
        "path": "/path/to/9709_s22_qp_12.pdf",
    }
    
    # Create a pydantic-like object for testing
    class ResourceCreate:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
        def dict(self):
            return self.__dict__

    resource_in = ResourceCreate(**resource_data)
    
    # The crud function expects a pydantic model, so we can't just pass a dict
    # We will need to adjust the crud function later to be more flexible
    # For now, let's adjust the test to work with the current crud function
    
    # This is a hack to make the test work without pydantic
    class TempResource:
        def dict(self):
            return resource_data
            
    crud.create_resource(db=db_session, resource=TempResource())

    retrieved_resource = crud.get_resource_by_path(db=db_session, path="/path/to/9709_s22_qp_12.pdf")

    assert retrieved_resource is not None
    assert retrieved_resource.subject == "Mathematics"
    assert retrieved_resource.year == 2022
    assert retrieved_resource.path == "/path/to/9709_s22_qp_12.pdf"

def test_create_learning_pack(db_session):
    """
    Test creating a learning pack and associating it with syllabus points.
    """
    # 1. Create a student
    student = models.Student(username="testuser")
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)

    # 2. Create some syllabus points
    sp1 = models.SyllabusPoint(subject="Accounting", code="9706/1.1", description="The accounting cycle")
    sp2 = models.SyllabusPoint(subject="Accounting", code="9706/1.2", description="Source documents")
    db_session.add_all([sp1, sp2])
    db_session.commit()
    db_session.refresh(sp1)
    db_session.refresh(sp2)

    # 3. Create the learning pack
    learning_pack = crud.create_learning_pack_with_syllabus(
        db=db_session, student_id=student.id, syllabus_point_ids=[sp1.id, sp2.id]
    )

    assert learning_pack is not None
    assert learning_pack.student_id == student.id
    assert len(learning_pack.syllabus_points) == 2
    assert sp1 in learning_pack.syllabus_points
    assert sp2 in learning_pack.syllabus_points
