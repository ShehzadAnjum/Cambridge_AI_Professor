import argparse
from pathlib import Path
from src.content_generation_engine.learning_pack_generator import generate_learning_pack
from src.content_generation_engine.exam_generator import generate_mock_exam
from src.core_database.database import SessionLocal
import sys
from typing import Generator

def get_db() -> Generator[SessionLocal, None, None]:
    """
    Dependency to get a database session.

    Yields:
        A SQLAlchemy SessionLocal object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main() -> None:
    """
    Main entry point for the Content Generation Engine CLI.
    Parses arguments and dispatches commands.
    """
    parser = argparse.ArgumentParser(description="Content Generation Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate Learning Pack command
    gen_lp_parser = subparsers.add_parser("gen-lp", help="Generate a learning pack")
    gen_lp_parser.add_argument("--student-id", type=int, required=True, help="ID of the student")
    gen_lp_parser.add_argument("--topics", nargs='+', required=True, help="List of syllabus topic codes")

    # Generate Mock Exam command
    gen_exam_parser = subparsers.add_parser("gen-exam", help="Generate a mock exam")
    gen_exam_parser.add_argument("--student-id", type=int, required=True, help="ID of the student")
    gen_exam_parser.add_argument("--subject", type=str, required=True, help="Subject code for the exam")
    gen_exam_parser.add_argument("--num-questions", type=int, default=10, help="Number of questions to include")
    
    args = parser.parse_args()

    db_generator = get_db()
    db = next(db_generator)

    try:
        if args.command == "gen-lp":
            print(f"Generating learning pack for student {args.student_id} with topics: {args.topics}")
            learning_pack = generate_learning_pack(
                student_id=args.student_id,
                syllabus_topic_codes=args.topics,
                db=db
            )
            if learning_pack:
                print(f"Successfully generated learning pack with ID: {learning_pack.id}")
            else:
                print("Failed to generate learning pack.", file=sys.stderr)
        elif args.command == "gen-exam":
            print(f"Generating mock exam for student {args.student_id}, subject {args.subject}")
            mock_exam = generate_mock_exam(
                student_id=args.student_id,
                subject=args.subject,
                num_questions=args.num_questions,
                db=db
            )
            if mock_exam:
                print(f"Successfully generated mock exam with ID: {mock_exam.id}")
            else:
                print("Failed to generate mock exam.", file=sys.stderr)
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
