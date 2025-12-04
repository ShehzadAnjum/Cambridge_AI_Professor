import argparse
import sys
from src.a_star_workflow_orchestrator.orchestrator import run_full_loop
from src.core_database.database import SessionLocal
from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    """
    Provides a database session to the CLI commands.
    This function is a dependency injector that ensures the database session
    is properly opened and closed for each command.

    Yields:
        A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main() -> None:
    """
    The main entry point for the Cambridge AI Professor CLI.
    This function parses command-line arguments and dispatches the appropriate
    command to the corresponding handler function.
    """
    parser = argparse.ArgumentParser(
        description="Cambridge AI Professor CLI",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start loop command
    start_loop_parser = subparsers.add_parser(
        "start-loop",
        help="Start a new learning loop for a student on a specific topic.",
        description="Example: cambridge-ai-professor start-loop --student-id 1 --topics 1.1 1.2"
    )
    start_loop_parser.add_argument("--student-id", type=int, required=True, help="ID of the student")
    start_loop_parser.add_argument("--topics", nargs='+', required=True, help="List of syllabus topic codes")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    db_generator = get_db()
    db = next(db_generator)

    try:
        if args.command == "start-loop":
            if not args.student_id or not args.topics:
                start_loop_parser.print_help()
                sys.exit(1)
            
            print(f"Starting new learning loop for student {args.student_id} with topics: {args.topics}...")
            run_full_loop(
                student_id=args.student_id,
                syllabus_topic_codes=args.topics,
                db=db
            )
            print("\nLearning loop completed successfully.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        next(db_generator, None) # Ensure the generator is consumed and session is closed

if __name__ == "__main__":
    main()
