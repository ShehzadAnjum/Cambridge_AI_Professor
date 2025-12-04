# Tasks: Content Generation Engine

**Input**: Design documents from `specs/003-content-generation-engine/`
**Prerequisites**: plan.md, spec.md, data-model.md

## Phase 1: Setup
- [X] T001 Create the `src/content_generation_engine` directory and `__init__.py`.
- [X] T002 Create `src/content_generation_engine/pdf_qa_extractor.py`.

## Phase 2: Foundational (PDF Question/Answer Extraction)
- [X] T003 Research existing Python libraries for advanced PDF parsing and question extraction (e.g., PyPDF2, pdfplumber, layoutparser, Tesseract OCR for image-based PDFs). Document findings in `research.md`.
- [X] T004 Implement initial `extract_questions_from_pdf(filepath: Path)` function in `src/content_generation_engine/pdf_qa_extractor.py`. This function should identify and extract question text and, if possible, `max_marks`. (Initial implementation can be a placeholder if advanced parsing is complex).
- [X] T005 Create initial tests for `pdf_qa_extractor.py` in `tests/test_pdf_qa_extractor.py`. These tests should cover basic text extraction and simple pattern matching for questions.

## Phase 3: User Story 1 - Generate Personalized Learning Pack (Priority: P1)
**Goal**: Produce a valid learning pack with associated resources and syllabus points.
**Independent Test**: The system can generate a learning pack, link it to a student, syllabus points, and relevant resources.

### Implementation for User Story 1
- [X] T006 Create `src/content_generation_engine/learning_pack_generator.py`.
- [X] T007 Implement `generate_learning_pack(student_id: int, syllabus_topic_codes: List[str], db: Session)` function in `src/content_generation_engine/learning_pack_generator.py`. This function should query `Resource` and `SyllabusPoint` tables, select relevant resources, and create a `LearningPack` entry using `core_database.crud`.
- [X] T008 Create tests for `learning_pack_generator.py` in `tests/test_learning_pack_generator.py`.

## Phase 4: User Story 2 - Generate Mock Examination (Priority: P1)
**Goal**: Produce a valid mock examination with a set of questions (with max marks).
**Independent Test**: The system can generate a mock exam and link it to a student and questions.

### Implementation for User Story 2
- [X] T009 Create `src/content_generation_engine/exam_generator.py`.
- [X] T010 Implement `generate_mock_exam(student_id: int, subject: str, num_questions: int, db: Session)` function in `src/content_generation_engine/exam_generator.py`. This function should use `pdf_qa_extractor` (or manually curated questions) to select `Question`s, and create a `MockExam` entry using `core_database.crud`.
- [X] T011 Create tests for `exam_generator.py` in `tests/test_exam_generator.py`.

## Phase 5: Polish & Cross-Cutting Concerns
- [X] T012 Add CLI commands to `src/content_generation_engine/main.py` for generating learning packs and mock exams. (This requires creating `main.py` if it doesn't exist).
- [X] T013 Integrate `pdf_qa_extractor` with `dynamic_resource_manager` to automatically extract questions from new past papers upon download.
- [X] T014 Add comprehensive error handling and logging.
- [X] T015 Add docstrings and type hints to all public functions.
