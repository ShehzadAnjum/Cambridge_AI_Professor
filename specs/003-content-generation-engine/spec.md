# Feature Specification: Content Generation Engine

**Feature Branch**: `003-content-generation-engine`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "Build a content generation engine that creates personalized learning packs and mock examinations from the resources available in the core database, as per Constitution Principle II."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Personalized Learning Pack (Priority: P1)
As the system, I need to generate a personalized learning pack for a student based on their progress and a selected syllabus topic, utilizing available resources in the database, so that the student receives targeted study material.

**Why this priority**: Directly supports the "Assign & Study" phase of the A*-Focused Workflow.
**Independent Test**: The system can produce a valid learning pack with associated resources and syllabus points for a given student and topic.

**Acceptance Scenarios**:
1.  **Given** a student is identified and a specific syllabus topic (e.g., "9706/1.1 - The accounting cycle") is selected, **When** the system generates a learning pack, **Then** a new `LearningPack` record is created in the database, linked to the student and the selected syllabus points, and includes references to relevant `Resource` files (e.g., past paper questions, mark scheme excerpts).
2.  **Given** there are no resources available in the database for a selected syllabus topic, **When** the system attempts to generate a learning pack, **Then** it informs the user that no resources are found for the topic and does not create an empty learning pack.

### User Story 2 - Generate Mock Examination (Priority: P1)
As the system, I need to generate a mock examination paper for a student based on a subject and optionally a set of syllabus topics, utilizing available past paper questions in the database, so that the student can be assessed on their knowledge.

**Why this priority**: Directly supports the "Create & Test" phase of the A*-Focused Workflow.
**Independent Test**: The system can produce a valid mock examination with a set of questions (with max marks) for a given student and subject.

**Acceptance Scenarios**:
1.  **Given** a student is identified and a subject (e.g., "9706 - Accounting") is chosen, **When** the system generates a mock examination, **Then** a new `MockExam` record is created in the database, linked to the student and containing a curated list of `Question` entities with their `max_marks`.
2.  **Given** there are insufficient questions in the database for a selected subject or topic to create a full mock examination, **When** the system attempts to generate the exam, **Then** it generates the exam with the available questions and warns the user about the limited scope, or suggests alternative topics.

## Requirements *(mandatory)*

### Functional Requirements
-   **FR-001**: The system MUST be able to query the core database to retrieve relevant `Resource` files based on subject, year, type (e.g., "Past Paper", "Mark Scheme"), and associated `SyllabusPoint`s.
-   **FR-002**: The system MUST be able to extract individual `Question`s and their `max_marks` from `Past Paper` PDF resources. (This might require OCR or advanced PDF parsing).
-   **FR-003**: The system MUST be able to create `LearningPack` entries in the core database, linking to a `Student`, multiple `SyllabusPoint`s, and relevant `Resource`s.
-   **FR-004**: The system MUST be able to create `MockExam` entries in the core database, linking to a `Student` and a curated list of `Question`s.
-   **FR-005**: The system MUST provide an interface (e.g., CLI function) to trigger learning pack generation.
-   **FR-006**: The system MUST provide an interface (e.g., CLI function) to trigger mock examination generation.

### Key Entities
-   **LearningPack**: (Already defined in core-database) Represents a collection of study materials.
-   **MockExam**: (Already defined in core-database) Represents a generated test.
-   **Question**: (Already defined in core-database) An individual question with its max marks.
-   **ContentGenerator**: A new component orchestrating the generation logic.
-   **PDFParser**: A sub-component within ContentGenerator responsible for extracting questions from PDFs.

## Success Criteria *(mandatory)*

### Measurable Outcomes
-   **SC-001**: A learning pack for a specific syllabus topic is generated successfully within 10 seconds, containing at least 3 relevant resources from the database, when resources are available.
-   **SC-002**: A mock examination for a given subject is generated successfully within 15 seconds, containing at least 5 unique questions, when questions are available.
-   **SC-003**: All generated `LearningPack` and `MockExam` records accurately reflect their associated `Student`, `SyllabusPoint`s, `Resource`s, and `Question`s in the core database.