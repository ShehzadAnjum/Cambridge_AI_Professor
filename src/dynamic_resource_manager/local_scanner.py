from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.dynamic_resource_manager.metadata_extractor import MetadataExtractor
from src.core_database import crud

def scan_local_directory(directory: Path, db: Session) -> None:
    """
    Scans a local directory for PDF files, extracts their metadata,
    and stores/updates them in the database.

    Args:
        directory: The path to the directory to scan.
        db: The database session.
    """
    metadata_extractor = MetadataExtractor()
    for filepath in directory.rglob("*.pdf"):
        metadata = metadata_extractor.extract_metadata_from_filename(filepath)
        if metadata:
            resource_data = {
                "subject": metadata["subject_code"],
                "year": int(metadata["year"]),
                "paper": int(metadata["paper"]),
                "variant": int(metadata["variant"]),
                "type": metadata["type"],
                "path": str(filepath.resolve()),
            }
            # Check if resource already exists
            existing_resource = crud.get_resource_by_path(db, resource_data["path"])
            if existing_resource:
                # Update last_seen timestamp
                existing_resource.last_seen = func.now()
                db.add(existing_resource) # Re-add to session to mark as modified
                db.commit()
                db.refresh(existing_resource)
                print(f"Updated existing resource: {filepath.name}")
            else:
                crud.create_resource(db, resource_data)
                print(f"Added new resource: {filepath.name}")
        else:
            print(f"Skipping {filepath.name}: Could not extract metadata from filename.")