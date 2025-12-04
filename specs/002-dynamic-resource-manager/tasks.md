# Tasks: Dynamic Resource Manager

**Input**: Design documents from `specs/002-dynamic-resource-manager/`
**Prerequisites**: plan.md, spec.md, data-model.md

## Phase 1: Setup
- [X] T001 Create the `src/dynamic_resource_manager` directory and `__init__.py`.
- [X] T002 Install required Python packages: `requests`, `beautifulsoup4`, `pdfminer.six`.
- [X] T003 Create `src/dynamic_resource_manager/metadata_extractor.py` and implement initial metadata extraction logic for filenames.

## Phase 2: Foundational (Metadata Extraction)
- [X] T004 Implement `extract_metadata_from_filename(filepath: Path)` function in `src/dynamic_resource_manager/metadata_extractor.py`. This function should parse filenames like `9706_s22_qp_12.pdf` to extract subject, year, paper type, and variant.
- [X] T005 Implement `extract_text_from_pdf(filepath: Path)` function in `src/dynamic_resource_manager/metadata_extractor.py` using `pdfminer.six`.
- [X] T006 Implement `get_metadata_from_pdf_content(filepath: Path)` function in `src/dynamic_resource_manager/metadata_extractor.py` to extract additional metadata (e.g., subject code from syllabus) from PDF text content.

## Phase 3: User Story 1 - Scan Local Resource Bank (Priority: P1)
**Goal**: Identify, extract metadata from, and persist details of local resource files.
**Independent Test**: The local scanner processes a directory and updates the database correctly.

### Implementation for User Story 1
- [X] T007 Create `src/dynamic_resource_manager/local_scanner.py`.
- [X] T008 Implement `scan_local_directory(directory: Path, db: Session)` function in `src/dynamic_resource_manager/local_scanner.py`. This function should iterate through files, call `metadata_extractor` functions, and use `core_database.crud` to store/update resources.
- [X] T009 Create initial tests for `local_scanner.py` in `tests/test_local_scanner.py`.
- [X] T010 Implement the CLI command `scan-local` in `src/dynamic_resource_manager/main.py` using `argparse` or `click` to trigger `scan_local_directory`.

## Phase 4: User Story 2 - Download Resources from Approved Web Sources (Priority: P1)
**Goal**: Connect to an approved web source, download a specified resource, and process its metadata.
**Independent Test**: The web scraper downloads a resource and processes its metadata, updating the database.

### Implementation for User Story 2
- [X] T011 Create `src/dynamic_resource_manager/web_scraper.py`.
- [X] T012 Implement `get_all_download_links(url: str)` function in `src/dynamic_resource_manager/web_scraper.py` using `requests` and `BeautifulSoup4` for `savemyexams.com` structure.
- [X] T013 Implement `download_file(url: str, save_path: Path)` function in `src/dynamic_resource_manager/web_scraper.py`.
- [X] T014 Implement `scrape_and_download(subject: str, year_range: tuple, db: Session)` function in `src/dynamic_resource_manager/web_scraper.py` that orchestrates link discovery, download, and database updates.
- [X] T015 Create initial tests for `web_scraper.py` in `tests/test_web_scraper.py`.
- [X] T016 Implement the CLI command `scrape-web` in `src/dynamic_resource_manager/main.py` to trigger `scrape_and_download`.

## Phase 5: Polish & Cross-Cutting Concerns
- [X] T017 Add comprehensive error handling and logging for all resource manager components.
- [X] T018 Ensure robust handling of existing files (update `last_seen` timestamp, avoid re-downloading if not newer).
- [X] T019 Add docstrings and type hints to all public functions.
