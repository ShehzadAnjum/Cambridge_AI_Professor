import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.core_database.database import Base
from src.core_database import crud, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dynamic_resource_manager import web_scraper

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

@patch('src.dynamic_resource_manager.web_scraper.get_all_download_links')
@patch('src.dynamic_resource_manager.web_scraper.download_file')
@patch('src.dynamic_resource_manager.web_scraper.MetadataExtractor.extract_metadata_from_filename')
def test_scrape_and_download(
    mock_extract_metadata,
    mock_download_file,
    mock_get_all_download_links,
    tmp_path: Path,
    db_session: Session
):
    # Setup mocks
    mock_get_all_download_links.return_value = [
        "https://www.savemyexams.com/download/9706_s22_qp_12.pdf",
        "https://www.savemyexams.com/download/9706_s22_ms_12.pdf",
    ]
    mock_download_file.return_value = True # Simulate successful download
    mock_extract_metadata.side_effect = [
        {'subject_code': '9706', 'season': 's', 'year': '2022', 'type': 'Past Paper', 'paper': '1', 'variant': '2'},
        {'subject_code': '9706', 'season': 's', 'year': '2022', 'type': 'Mark Scheme', 'paper': '1', 'variant': '2'}
    ]

    # Execute
    web_scraper.scrape_and_download(
        subject_code="Accounting_9706",
        year_range=(2022, 2022),
        db=db_session,
        base_resource_path=tmp_path
    )

    # Verify
    assert mock_get_all_download_links.called
    assert mock_download_file.call_count == 2
    assert mock_extract_metadata.call_count == 2

    resource_qp = crud.get_resource_by_path(db_session, str((tmp_path / "9706_Past Paper/2022/9706_s22_qp_12.pdf").resolve()))
    resource_ms = crud.get_resource_by_path(db_session, str((tmp_path / "9706_Mark Scheme/2022/9706_s22_ms_12.pdf").resolve()))

    assert resource_qp is not None
    assert resource_qp.subject == "9706"
    assert resource_qp.type == "Past Paper"

    assert resource_ms is not None
    assert resource_ms.subject == "9706"
    assert resource_ms.type == "Mark Scheme"

    # Test year range filtering
    db_session.rollback() # Clear previous state
    mock_get_all_download_links.reset_mock()
    mock_download_file.reset_mock()
    mock_extract_metadata.reset_mock()

    mock_get_all_download_links.return_value = [
        "https://www.savemyexams.com/download/9706_s22_qp_12.pdf",
        "https://www.savemyexams.com/download/9706_s23_qp_12.pdf", # This one should be filtered out
    ]
    mock_download_file.return_value = True
    mock_extract_metadata.side_effect = [
        {'subject_code': '9706', 'season': 's', 'year': '2022', 'type': 'Past Paper', 'paper': '1', 'variant': '2'},
        {'subject_code': '9706', 'season': 's', 'year': '2023', 'type': 'Past Paper', 'paper': '1', 'variant': '2'}
    ]

    web_scraper.scrape_and_download(
        subject_code="Accounting_9706",
        year_range=(2022, 2022),
        db=db_session,
        base_resource_path=tmp_path
    )
    assert mock_download_file.call_count == 1 # Only one file should be downloaded (2022)
    resource_2023 = crud.get_resource_by_path(db_session, str((tmp_path / "9706_Past Paper/2023/9706_s23_qp_12.pdf").resolve()))
    assert resource_2023 is None # Should not be in DB
