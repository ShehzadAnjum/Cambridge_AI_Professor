import pytest
from unittest.mock import patch, MagicMock
from src.cli import main
import sys

@patch('src.cli.main.run_full_loop')
@patch('src.cli.main.get_db')
def test_cli_start_loop(mock_get_db, mock_run_full_loop):
    """
    Tests the 'start-loop' command of the CLI.
    """
    # Mock the database session
    mock_db = MagicMock()
    
    # Create a generator for the mock
    def mock_db_generator():
        yield mock_db
        
    mock_get_db.return_value = mock_db_generator()

    # Simulate command line arguments
    sys.argv = ['cambridge-ai-professor', 'start-loop', '--student-id', '1', '--topics', '1.1', '1.2']
    
    main.main()

    # Verify that the orchestrator function was called with the correct arguments
    mock_run_full_loop.assert_called_once_with(
        student_id=1,
        syllabus_topic_codes=['1.1', '1.2'],
        db=mock_db
    )

@patch('argparse.ArgumentParser.print_help')
def test_cli_no_command(mock_print_help):
    """
    Tests the CLI with no command provided.
    """
    sys.argv = ['cambridge-ai-professor']
    main.main()
    mock_print_help.assert_called_once()