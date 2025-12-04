# Implementation Plan: Content Generation Engine

**Branch**: `003-content-generation-engine` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/003-content-generation-engine/spec.md`

## Summary
This plan outlines the technical approach for building the content generation engine. It will leverage the core database for resource and syllabus information. The primary challenge identified is the extraction of questions and their marks from PDF past papers (FR-002), which will require research into PDF parsing and potentially OCR techniques. The engine will provide functions for creating learning packs and mock exams, interacting with the database.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `pdfminer.six` (for basic PDF text extraction), potential new libraries for advanced PDF parsing/OCR (to be researched). `SQLAlchemy` (for database interaction). `numpy` for data manipulation.
**Storage**: Core database (SQLite in development)
**Testing**: `pytest`, `unittest.mock`
**Target Platform**: Local execution environment (Linux)
**Project Type**: Single project (library-style module)
**Performance Goals**:
- Learning pack generation: < 10 seconds.
- Mock examination generation: < 15 seconds.
**Constraints**:
- Must integrate seamlessly with the `core_database` module.
- `FR-002` (question extraction from PDFs) is a significant technical challenge and a potential blocker; extensive research and prototyping are required.
**Scale/Scope**: Generate content for a single student across multiple subjects and years.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [X] Principle I (Dynamic Resource Management): This engine consumes resources managed by the dynamic resource manager.
- [X] Principle II (On-the-Fly Content Generation): This feature directly implements the generation of learning packs and mock examinations.
- [X] Principle III (Persistent State Tracking): Directly interacts with the core database to store generated content (LearningPacks, MockExams).
- [X] Principle IV (A*-Focused Workflow): Provides the "Assign & Study" and "Create & Test" components of the workflow.

## Project Structure

### Documentation (this feature)

```text
specs/003-content-generation-engine/
├── plan.md              # This file
├── research.md          # To be generated (focused on PDF question extraction)
├── data-model.md        # Not needed (uses core-database data model)
├── quickstart.md        # To be generated
└── tasks.md             # To be generated
```

### Source Code (repository root)

```text
src/
├── content_generation_engine/
│   ├── __init__.py
│   ├── learning_pack_generator.py # Generates learning packs
│   ├── exam_generator.py          # Generates mock exams
│   ├── pdf_qa_extractor.py        # Extracts questions/answers from PDFs (FR-002)
│   └── main.py                    # CLI entry point (if any)
├── core_database/                 # Existing module
├── dynamic_resource_manager/      # Existing module
└── tests/
    ├── test_learning_pack_generator.py
    ├── test_exam_generator.py
    └── test_pdf_qa_extractor.py
```

**Structure Decision**: A new `content_generation_engine` module will be created under `src`, containing sub-modules for learning pack generation, exam generation, and a dedicated component for PDF question/answer extraction. This modular approach helps isolate the complex PDF parsing logic.

## Complexity Tracking
No constitutional violations detected.