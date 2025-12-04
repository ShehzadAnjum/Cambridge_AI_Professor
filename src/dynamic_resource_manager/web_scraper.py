import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from pathlib import Path
import re
from sqlalchemy.orm import Session
from src.core_database import crud
from src.dynamic_resource_manager.metadata_extractor import MetadataExtractor

BASE_URLS = {
    "Accounting_9706": "https://www.savemyexams.com/a-level/accounting/cie/9706/past-papers/",
    "Economics_9708": "https://www.savemyexams.com/a-level/economics/cie/9708/past-papers/",
    "Mathematics_9709": "https://www.savemyexams.com/a-level/maths/cie/9709/past-papers/",
    "English_General_Paper_8021": "https://www.savemyexams.com/a-level/english-general-paper/cie/8021/past-papers/",
}

def get_all_download_links(url: str) -> List[str]:
    """
    Extracts all PDF download links from a given URL on savemyexams.com.

    Args:
        url: The URL of the page to scrape.

    Returns:
        A list of absolute URLs to PDF files.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = []
    
    # Save My Exams download links often contain "download" in the href
    # And are usually within <a> tags.
    # Example structure: <a href=".../download/...">...</a>
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if ".pdf" in href and "download" in href:
            # Construct absolute URL if it's relative
            if not href.startswith("http"):
                href = requests.compat.urljoin(url, href)
            download_links.append(href)
    
    return download_links

def download_file(url: str, save_path: Path) -> bool:
    """
    Downloads a file from a given URL and saves it to the specified path.

    Args:
        url: The URL of the file to download.
        save_path: The full path including filename to save the downloaded file.

    Returns:
        True if the download was successful, False otherwise.
    """
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False
    except IOError as e:
        print(f"Error writing file to {save_path}: {e}")
        return False

def scrape_and_download(
    subject_code: str,
    year_range: Optional[Tuple[int, int]],
    db: Session,
    base_resource_path: Path = Path("./resource_bank")
) -> None:
    """
    Orchestrates the scraping and downloading of resources for a given subject.

    Args:
        subject_code: The subject code (e.g., "9706") to scrape.
        year_range: A tuple indicating the start and end year (inclusive) to download for.
                    If None, downloads all available years.
        db: The database session.
        base_resource_path: The base path where resources should be saved.
    """
    if subject_code not in BASE_URLS:
        print(f"Error: Subject code {subject_code} not configured for web scraping.")
        return

    base_url = BASE_URLS[subject_code]
    print(f"Starting web scrape for {subject_code} from {base_url}")
    
    links = get_all_download_links(base_url)
    metadata_extractor = MetadataExtractor()

    for link in links:
        filename = Path(link).name
        metadata = metadata_extractor.extract_metadata_from_filename(Path(filename))

        if metadata:
            file_year = int(metadata.get('year', 0))
            if year_range and not (year_range[0] <= file_year <= year_range[1]):
                print(f"Skipping {filename}: outside specified year range {year_range}")
                continue
            
            # Construct save path: resource_bank/Subject_Code/Type/Year/filename.pdf
            save_dir = base_resource_path / f"{metadata['subject_code']}_{metadata['type']}" / str(metadata['year'])
            save_path = save_dir / filename

            existing_resource = crud.get_resource_by_path(db, str(save_path.resolve()))
            if existing_resource:
                print(f"Resource already exists, skipping download: {filename}")
                continue

            print(f"Downloading {filename} to {save_path}...")
            if download_file(link, save_path):
                resource_data = {
                    "subject": metadata["subject_code"],
                    "year": int(metadata["year"]),
                    "paper": int(metadata["paper"]),
                    "variant": int(metadata["variant"]),
                    "type": metadata["type"],
                    "path": str(save_path.resolve()),
                }
                crud.create_resource(db, resource_data)
                print(f"Successfully downloaded and added to DB: {filename}")
            else:
                print(f"Failed to download {filename}")
        else:
            print(f"Skipping {filename}: Could not extract metadata from link name.")
