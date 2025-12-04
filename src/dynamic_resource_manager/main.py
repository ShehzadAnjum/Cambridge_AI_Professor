import argparse
from pathlib import Path
from src.dynamic_resource_manager.local_scanner import scan_local_directory
from src.dynamic_resource_manager.web_scraper import scrape_and_download
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
    Main entry point for the Dynamic Resource Manager CLI.
    Parses arguments and dispatches commands.
    """
    parser = argparse.ArgumentParser(description="Dynamic Resource Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Local scan command
    scan_local_parser = subparsers.add_parser("scan-local", help="Scan local directory for resources")
    scan_local_parser.add_argument("directory", type=str, help="Path to the directory to scan")

    # Web scrape command
    scrape_web_parser = subparsers.add_parser("scrape-web", help="Scrape web sources for resources")
    scrape_web_parser.add_argument("--subject", type=str, required=True, help="Subject code (e.g., Accounting_9706)")
    scrape_web_parser.add_argument("--year-start", type=int, help="Start year for scraping (inclusive)")
    scrape_web_parser.add_argument("--year-end", type=int, help="End year for scraping (inclusive)")

    args = parser.parse_args()

    db_generator = get_db()
    db = next(db_generator)

    try:
        if args.command == "scan-local":
            directory_path = Path(args.directory)
            if not directory_path.is_dir():
                print(f"Error: Directory '{directory_path}' not found.", file=sys.stderr)
                sys.exit(1)
            print(f"Scanning local directory: {directory_path}")
            scan_local_directory(directory_path, db)
            print("Local scan completed.")
        elif args.command == "scrape-web":
            year_range = (args.year_start, args.year_end) if args.year_start and args.year_end else None
            print(f"Initiating web scrape for subject: {args.subject}, years: {year_range}")
            scrape_and_download(args.subject, year_range, db)
            print("Web scraping completed.")
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
