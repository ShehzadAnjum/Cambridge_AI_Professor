import argparse
from src.a_star_workflow_orchestrator.orchestrator import run_full_loop
from src.core_database.database import SessionLocal
import sys
from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main() -> None:
    """
    Main entry point for the A*-Workflow Orchestrator CLI.
    """
    parser = argparse.ArgumentParser(description="A*-Workflow Orchestrator CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start loop command
    start_loop_parser = subparsers.add_parser("start-loop", help="Start a new learning loop")
    start_loop_parser.add_argument("--student-id", type=int, required=True, help="ID of the student")
    start_loop_parser.add_argument("--topics", nargs='+', required=True, help="List of syllabus topic codes")
    
    # NOTE: resume-loop is not implemented in this version as it requires more complex state management
    # resume_loop_parser = subparsers.add_parser("resume-loop", help="Resume an in-progress learning loop")
    # resume_loop_parser.add_argument("--student-id", type=int, required=True, help="ID of the student")

    args = parser.parse_args()

    db_generator = get_db()
    db = next(db_generator)

    try:
        if args.command == "start-loop":
            print(f"Starting new learning loop for student {args.student_id} with topics: {args.topics}")
            run_full_loop(
                student_id=args.student_id,
                syllabus_topic_codes=args.topics,
                db=db
            )
            print("Learning loop completed.")
        else:
            parser.print_help()
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            db_generator.throw(None) # Close the session
        except StopIteration:
            pass

if __name__ == "__main__":
    main()
