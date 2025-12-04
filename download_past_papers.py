#!/usr/bin/env python3
"""
Script to download A-Level past papers, mark schemes, and examiner reports
from gceguide.com and organize them by subject and year.
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent / "resource_bank"
SUBJECTS = {
    "Accounting_9706": "https://gceguide.com/past-papers/A-AS-Level/Accounting-9706/",
    "Economics_9708": "https://gceguide.com/past-papers/A-AS-Level/Economics-9708/",
    "Mathematics_9709": "https://gceguide.com/past-papers/A-AS-Level/Mathematics-9709/",
    "English_General_Paper_8021": "https://gceguide.com/past-papers/A-AS-Level/English-General-Paper-8021/"
}

YEARS_TO_DOWNLOAD = 5  # Last 5 years
DELAY = 2  # Delay between requests to be respectful

# Headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def get_current_years():
    """Get the last 5 years from current year."""
    from datetime import datetime
    current_year = datetime.now().year
    return list(range(current_year, current_year - YEARS_TO_DOWNLOAD, -1))

def sanitize_filename(filename):
    """Sanitize filename for filesystem."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename

def download_file(url, filepath, retries=3):
    """Download a file from URL to filepath."""
    for attempt in range(retries):
        try:
            print(f"  Downloading: {os.path.basename(filepath)}")
            response = requests.get(url, stream=True, timeout=30, headers=HEADERS)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✓ Downloaded: {os.path.basename(filepath)}")
            return True
        except Exception as e:
            if attempt < retries - 1:
                print(f"  ⚠ Retry {attempt + 1}/{retries} for {os.path.basename(filepath)}...")
                time.sleep(DELAY * (attempt + 1))
            else:
                print(f"  ✗ Error downloading {url}: {e}")
                return False
    return False

def find_pdf_links(soup, base_url):
    """Find all PDF links on the page."""
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Check if it's a PDF link
        if href.lower().endswith('.pdf') or 'pdf' in href.lower():
            full_url = urljoin(base_url, href)
            pdf_links.append((full_url, link.get_text(strip=True)))
    return pdf_links

def categorize_file(filename, link_text):
    """Categorize file as Past Paper, Mark Scheme, or Examiner Report."""
    filename_lower = filename.lower()
    text_lower = link_text.lower()
    combined = f"{filename_lower} {text_lower}"
    
    if any(term in combined for term in ['mark scheme', 'markscheme', 'ms', 'marking']):
        return 'Mark_Scheme'
    elif any(term in combined for term in ['examiner report', 'examiner', 'er', 'report']):
        return 'Examiner_Report'
    elif any(term in combined for term in ['past paper', 'question paper', 'qp', 'paper']):
        return 'Past_Paper'
    else:
        return 'Other'

def extract_year_from_filename(filename):
    """Extract year from filename."""
    # Look for 4-digit years (2000-2099)
    years = re.findall(r'\b(20\d{2})\b', filename)
    if years:
        return int(years[-1])  # Return the last (most recent) year found
    return None

def process_subject(subject_name, url):
    """Process a single subject's page."""
    print(f"\n{'='*60}")
    print(f"Processing: {subject_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        # Fetch the main page with retries
        response = None
        for attempt in range(5):  # More retries
            try:
                print(f"  Attempting to fetch page (attempt {attempt + 1}/5)...")
                response = requests.get(url, timeout=60, headers=HEADERS)  # Longer timeout
                # Check status code before raising
                if response.status_code == 522:
                    if attempt < 4:
                        wait_time = DELAY * (attempt + 1) * 2
                        print(f"  ⚠ Server error (522), retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"  ✗ Server error (522) after {attempt + 1} attempts. Website may be down.")
                        return
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response else None
                if status_code == 522 and attempt < 4:
                    wait_time = DELAY * (attempt + 1) * 2  # Longer waits
                    print(f"  ⚠ Server error (522), retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue  # Continue to next attempt
                elif attempt < 4:
                    wait_time = DELAY * (attempt + 1)
                    print(f"  ⚠ HTTP error ({status_code}), retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise
            except requests.exceptions.RequestException as e:
                if attempt < 4:
                    wait_time = DELAY * (attempt + 1) * 2
                    print(f"  ⚠ Connection error, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
        
        if not response or response.status_code != 200:
            print(f"  ✗ Could not fetch page after retries")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all PDF links
        pdf_links = find_pdf_links(soup, url)
        print(f"Found {len(pdf_links)} PDF links")
        
        if not pdf_links:
            print("  No PDF links found. Checking for year-specific pages...")
            # Look for year links
            year_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                # Check if it looks like a year link
                if re.search(r'\b(20\d{2})\b', text) or re.search(r'\b(20\d{2})\b', href):
                    full_url = urljoin(url, href)
                    year_links.append((full_url, text))
            
            if year_links:
                print(f"  Found {len(year_links)} potential year pages")
                # Process each year page
                for year_url, year_text in year_links[:20]:  # Limit to avoid too many requests
                    year_match = re.search(r'\b(20\d{2})\b', year_text or year_url)
                    if year_match:
                        year = int(year_match.group(1))
                        if year in get_current_years():
                            print(f"\n  Processing year {year} page...")
                            time.sleep(DELAY)
                            process_year_page(subject_name, year, year_url)
            return
        
        # Organize files by year
        target_years = get_current_years()
        files_by_year = {year: [] for year in target_years}
        
        for pdf_url, link_text in pdf_links:
            filename = os.path.basename(urlparse(pdf_url).path) or "file.pdf"
            year = extract_year_from_filename(filename or link_text)
            
            if year and year in target_years:
                file_type = categorize_file(filename, link_text)
                files_by_year[year].append((pdf_url, filename, file_type))
        
        # Download files organized by year
        for year in target_years:
            if files_by_year[year]:
                print(f"\n  Year {year}: Found {len(files_by_year[year])} files")
                year_dir = BASE_DIR / subject_name / str(year)
                
                for pdf_url, filename, file_type in files_by_year[year]:
                    # Create subdirectory for file type
                    type_dir = year_dir / file_type
                    filepath = type_dir / sanitize_filename(filename)
                    
                    # Skip if file already exists
                    if filepath.exists():
                        print(f"  ⊘ Skipping (exists): {filename}")
                        continue
                    
                    time.sleep(DELAY)
                    download_file(pdf_url, filepath)
            else:
                print(f"\n  Year {year}: No files found")
        
    except Exception as e:
        print(f"  ✗ Error processing {subject_name}: {e}")
        import traceback
        traceback.print_exc()

def process_year_page(subject_name, year, year_url):
    """Process a specific year's page."""
    try:
        # Fetch with retries
        response = None
        for attempt in range(3):
            try:
                response = requests.get(year_url, timeout=30, headers=HEADERS)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 522 and attempt < 2:
                    time.sleep(DELAY * (attempt + 1))
                else:
                    raise
        
        if not response or response.status_code != 200:
            print(f"    ✗ Could not fetch year {year} page after retries")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        pdf_links = find_pdf_links(soup, year_url)
        print(f"    Found {len(pdf_links)} PDF links for {year}")
        
        year_dir = BASE_DIR / subject_name / str(year)
        
        for pdf_url, link_text in pdf_links:
            filename = os.path.basename(urlparse(pdf_url).path) or "file.pdf"
            file_type = categorize_file(filename, link_text)
            
            # Create subdirectory for file type
            type_dir = year_dir / file_type
            filepath = type_dir / sanitize_filename(filename)
            
            # Skip if file already exists
            if filepath.exists():
                print(f"    ⊘ Skipping (exists): {filename}")
                continue
            
            time.sleep(DELAY)
            download_file(pdf_url, filepath)
            
    except Exception as e:
        print(f"    ✗ Error processing year {year} page: {e}")

def main():
    """Main function."""
    print("A-Level Past Papers Downloader")
    print("=" * 60)
    print(f"Target directory: {BASE_DIR}")
    print(f"Years to download: {get_current_years()}")
    print("=" * 60)
    
    # Create base directory
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Process each subject
    for subject_name, url in SUBJECTS.items():
        process_subject(subject_name, url)
        time.sleep(DELAY * 2)  # Extra delay between subjects
    
    print("\n" + "=" * 60)
    print("Download complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()



