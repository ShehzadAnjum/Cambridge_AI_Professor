# Feature Specification: Core Database Schema

**Feature Branch**: `001-core-database`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "Define and initialize the core database schema for state tracking, covering resource inventory, syllabus coverage, student progress, and assessment data as per Constitution Principle III."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - System Records a New Resource (Priority: P1)
As the system's Resource Manager, I need to persist the metadata of a discovered educational resource (like a past paper PDF) so that it can be inventoried and used for content generation.

**Why this priority**: This is the foundational capability for tracking what the system knows. Without it, no other function is possible.
**Independent Test**: The system can successfully add a new resource record to the database and retrieve it, proving it has been durably stored.

**Acceptance Scenarios**:
1.  **Given** the database is running, **When** the system discovers a new PDF resource, **Then** a new record is created in the `resources` table with its subject, year, type, and local path.
2.  **Given** a resource with a specific path already exists, **When** the system attempts to add the same resource, **Then** the existing record is updated (e.g., with a new `last_seen` timestamp) and a duplicate is not created.

### User Story 2 - System Tracks Syllabus Coverage (Priority: P2)
As the system's A-Star Orchestrator, I need to log which specific syllabus points have been covered in a learning pack so that I can plan future lessons and avoid repetition.

**Why this priority**: Tracks educational progress and informs the core planning loop.
**Independent Test**: The system can associate a learning pack with multiple syllabus points and mark them as "covered".

**Acceptance Scenarios**:
1.  **Given** a `learning_pack` and several `syllabus_points` exist, **When** a learning pack is generated, **Then** entries are created in a `coverage` join table linking the pack to each syllabus point.

## Requirements *(mandatory)*

### Functional Requirements
-   **FR-001**: The system MUST have a `resources` table to store metadata about educational materials, including subject, year, paper, variant, type (e.g., Past Paper, Mark Scheme), and file path.
-   **FR-002**: The system MUST have a `syllabus_points` table to store individual, trackable items from the official subject syllabuses.
-   **FR-003**: The system MUST have a `students` table to store basic student information.
-   **FR-004**: The system MUST have tables for tracking student progress, including `learning_packs`, `mock_exams`, and `exam_attempts`.
-   **FR-005**: The system MUST have tables for storing assessment data, linking student attempts to specific questions and recording scores and diagnosed weaknesses.
-   **FR-006**: The database schema MUST enforce uniqueness for resource paths to prevent duplicate entries.

### Key Entities
-   **Resource**: A single educational file (e.g., a PDF). Attributes: subject, year, type, path.
-   **SyllabusPoint**: A specific item from a subject's syllabus. Attributes: subject, code, description.
-   **Student**: The user of the system.
-   **LearningPack**: A collection of resources for a study session.
-   **MockExam**: A generated test paper.
-   **ExamAttempt**: A student's submission for a mock exam, including their answers and scores.

## Success Criteria *(mandatory)*

### Measurable Outcomes
-   **SC-001**: A database schema can be successfully initialized from a SQL script or ORM migration files.
-   **SC-002**: All data entities defined in the functional requirements can be created, read, updated, and deleted (CRUD) through a data access layer.
-   **SC-003**: The database MUST support relationships required by the A*-Workflow, such as linking a student's exam attempt to the specific questions and the resources used to generate them.