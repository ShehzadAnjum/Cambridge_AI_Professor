import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.dynamic_resource_manager import local_scanner
from src.core_database.database import Base
from src.core_database import crud, models
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

@patch('src.dynamic_resource_manager.metadata_extractor.MetadataExtractor.extract_metadata_from_filename')
def test_scan_local_directory(mock_extract_metadata, tmp_path: Path, db_session: Session):
    # Setup: Create dummy PDF files
    dummy_pdf_path1 = tmp_path / "9706_s22_qp_12.pdf"
    dummy_pdf_path1.write_text("dummy content")
    dummy_pdf_path2 = tmp_path / "9708_w23_ms_31.pdf"
    dummy_pdf_path2.write_text("dummy content")
    
    # Simulate metadata extraction
    mock_extract_metadata.side_effect = [
        {'subject_code': '9706', 'season': 's', 'year': '2022', 'type': 'Past Paper', 'paper': '1', 'variant': '2'},
        {'subject_code': '9708', 'season': 'w', 'year': '2023', 'type': 'Mark Scheme', 'paper': '3', 'variant': '1'}
    ]

    # Execute the scan
    local_scanner.scan_local_directory(tmp_path, db_session)

    # Verify: Check if resources are added to the database
    resource1 = crud.get_resource_by_path(db_session, str(dummy_pdf_path1.resolve()))
    resource2 = crud.get_resource_by_path(db_session, str(dummy_pdf_path2.resolve()))

    assert resource1 is not None
    assert resource1.subject == '9706'
    assert resource1.year == 2022
    assert resource1.type == 'Past Paper'
    assert resource1.path == str(dummy_pdf_path1.resolve())

    assert resource2 is not None
    assert resource2.subject == '9708'
    assert resource2.year == 2023
    assert resource2.type == 'Mark Scheme'
    assert resource2.path == str(dummy_pdf_path2.resolve())

    # Test update of existing resource (simulate second scan)
    mock_extract_metadata.side_effect = [
        {'subject_code': '9706', 'season': 's', 'year': '2022', 'type': 'Past Paper', 'paper': '1', 'variant': '2'},
        {'subject_code': '9708', 'season': 'w', 'year': '2023', 'type': 'Mark Scheme', 'paper': '3', 'variant': '1'}
    ]
    with patch('src.dynamic_resource_manager.local_scanner.func.now') as mock_func_now:
        mock_func_now.return_value = datetime(2025, 12, 4, 10, 0, 0)
        local_scanner.scan_local_directory(tmp_path, db_session)
    updated_resource = crud.get_resource_by_path(db_session, str(dummy_pdf_path1.resolve()))
    assert updated_resource.last_seen is not None # Should be updated
    assert updated_resource.subject == '9706' # Still the same subject
