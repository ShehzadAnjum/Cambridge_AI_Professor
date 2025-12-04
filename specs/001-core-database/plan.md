# Implementation Plan: Core Database

**Branch**: `001-core-database` | **Date**: 2025-12-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-core-database/spec.md`

## Summary
This plan outlines the technical approach for creating the core database of the A-Level Learning System. The database will use Python with SQLAlchemy and SQLite for simplicity and ease of setup, and will be designed to fulfill the state-tracking requirements of Constitution Principle III.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: SQLAlchemy (as the ORM), Alembic (for database migrations)
**Storage**: SQLite (for initial development, with the ability to switch to PostgreSQL later)
**Testing**: pytest
**Target Platform**: Local execution environment (Linux)
**Project Type**: Single project (library-style module)
**Performance Goals**: N/A for initial schema setup
**Constraints**: The schema must be extensible to support future features without major refactoring.
**Scale/Scope**: The initial design will support a single student and a few hundred resources.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [X] Principle I (Dynamic Resource Management): The schema includes a `resources` table.
- [X] Principle II (On-the-Fly Content Generation): The schema supports linking resources to generated content like `learning_packs`.
- [X] Principle III (Persistent State Tracking): The entire plan is focused on creating the means for persistent state tracking.
- [X] Principle IV (A*-Focused Workflow): The schema includes tables for `mock_exams`, `exam_attempts`, and `diagnosed_weaknesses` to support the workflow.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-database/
├── plan.md              # This file
├── research.md          # Not needed for this feature
├── data-model.md        # To be generated
├── quickstart.md        # To be generated
└── tasks.md             # To be generated
```

### Source Code (repository root)

```text
# Option 1: Single project (DEFAULT)
src/
├── core_database/
│   ├── __init__.py
│   ├── models.py      # SQLAlchemy ORM models
│   ├── crud.py        # Create, Read, Update, Delete operations
│   └── database.py    # Database session and engine setup
└── alembic/           # Alembic migration scripts
    ├── versions/
    └── env.py

tests/
├── test_core_database.py
```

**Structure Decision**: A dedicated `core_database` module will be created within the `src` directory to encapsulate all database-related logic. This promotes modularity and separation of concerns.

## Complexity Tracking
No constitutional violations detected.