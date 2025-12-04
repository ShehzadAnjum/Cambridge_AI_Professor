# Feature Specification: Dynamic Resource Manager

**Feature Branch**: `002-dynamic-resource-manager`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "Implement a dynamic resource manager that scans local directories (resource_bank) and approved web sources (e.g., Save My Exams) for educational materials, extracts metadata, and updates the core database as per Constitution Principle I."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Scan Local Resource Bank (Priority: P1)
As the system, I need to scan predefined local directories for educational resources so that they can be cataloged in the database.

**Why this priority**: Local resource management is the most straightforward and provides immediate value with existing data.
**Independent Test**: The system can correctly identify, extract metadata from, and persist details of local resource files.

**Acceptance Scenarios**:
1.  **Given** a local `resource_bank` directory contains various PDF files (past papers, mark schemes, syllabuses), **When** the resource manager initiates a local scan, **Then** metadata (subject, year, type, path) is extracted from each file and stored/updated in the core database `resources` table.
2.  **Given** a local `resource_bank` has previously scanned files, **When** a new scan is performed and a file has been updated or removed, **Then** the database reflects these changes (e.g., `last_seen` updated, old entries marked inactive/deleted).
3.  **Given** a local scan identifies a malformed file (e.g., unreadable PDF, incorrect naming convention), **When** the resource manager processes it, **Then** it logs an error but continues processing other files, and does not add the malformed file to the database.

### User Story 2 - Download Resources from Approved Web Sources (Priority: P1)
As the system, I need to download educational resources from approved web sources (e.g., Save My Exams) so that the resource bank is kept up-to-date with the latest available materials.

**Why this priority**: Web scraping ensures the resource bank grows and stays current.
**Independent Test**: The system can successfully connect to an approved web source, download a specified resource, and process its metadata.

**Acceptance Scenarios**:
1.  **Given** an approved web source URL for a subject's past papers (e.g., Save My Exams for Accounting 9706), **When** the resource manager initiates a web scrape for a specific year and paper, **Then** relevant PDF files are downloaded and saved to the local `resource_bank`, and their metadata is persisted to the core database.
2.  **Given** a web scrape encounters an unavailable resource or network error, **When** the resource manager attempts to download it, **Then** it logs the error, skips the unavailable resource, and continues with other downloads.
3.  **Given** a downloaded resource already exists locally or in the database, **When** the resource manager processes it, **Then** it updates the `last_seen` timestamp and skips re-downloading or creating duplicate entries unless the remote version is newer (optional, for later refinement).

## Requirements *(mandatory)*

### Functional Requirements
-   **FR-001**: The system MUST provide a command-line interface (CLI) to initiate a local scan of the `resource_bank` directory.
-   **FR-002**: The system MUST provide a CLI to initiate downloading of resources from approved web sources, specifying subject, year range, and resource type.
-   **FR-003**: The system MUST be able to extract metadata (subject, year, paper, variant, type, path) from file names of scanned/downloaded PDFs.
-   **FR-004**: The system MUST store/update extracted resource metadata in the `resources` table of the core database.
-   **FR-005**: The system MUST handle cases where files are unreadable or metadata extraction fails, logging errors without halting the process.
-   **FR-006**: The system MUST avoid duplicate entries in the database for the same resource path.
-   **FR-007**: The system MUST save downloaded web resources to the appropriate subdirectories within the local `resource_bank`.

### Key Entities
-   **Resource**: (Already defined in core-database) Metadata extracted from files.
-   **LocalFileScanner**: A component responsible for iterating through local directories and identifying resource files.
-   **WebScraper**: A component responsible for connecting to web sources, identifying download links, and downloading files.

## Success Criteria *(mandatory)*

### Measurable Outcomes
-   **SC-001**: A local scan of a populated `resource_bank` directory successfully identifies and processes 95% of valid resource files.
-   **SC-002**: A web scrape for a known set of resources from an approved source (e.g., Save My Exams) successfully downloads and processes 90% of available files.
-   **SC-003**: All extracted metadata is consistently stored in the core database `resources` table without duplicates for unique file paths.