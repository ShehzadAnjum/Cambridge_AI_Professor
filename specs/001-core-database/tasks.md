# Tasks: Core Database

**Input**: Design documents from `specs/001-core-database/`
**Prerequisites**: plan.md, spec.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)
- [X] T001 Initialize `alembic` for database migrations in the `src/` directory.
- [X] T002 Configure `alembic/env.py` to use the SQLite database connection.
- [X] T003 Create the main database engine and session management in `src/core_database/database.py`.

## Phase 2: Foundational (Blocking Prerequisites)
- [X] T004 Implement the `Student` SQLAlchemy model in `src/core_database/models.py`.
- [X] T005 Implement the `Resource` SQLAlchemy model in `src/core_database/models.py`.
- [X] T006 Implement the `SyllabusPoint` SQLAlchemy model in `src/core_database/models.py`.

## Phase 3: User Story 1 - System Records a New Resource (Priority: P1)
**Goal**: Persist discovered educational resources.
**Independent Test**: A new resource can be added and retrieved via a CRUD function.

### Implementation for User Story 1
- [X] T007 Generate the first alembic migration script to create the initial tables (`students`, `resources`, `syllabus_points`).
- [X] T008 Apply the migration to create the tables in the SQLite database.
- [X] T009 [P] Create a CRUD function `create_resource()` in `src/core_database/crud.py`.
- [X] T010 [P] Create a CRUD function `get_resource_by_path()` in `src/core_database/crud.py`.
- [X] T011 Create a basic test in `tests/test_core_database.py` to verify that `create_resource` and `get_resource_by_path` work as expected.

## Phase 4: User Story 2 - System Tracks Syllabus Coverage (Priority: P2)
**Goal**: Log which syllabus points are covered in a learning pack.
**Independent Test**: A learning pack can be successfully associated with syllabus points.

### Implementation for User Story 2
- [X] T012 Implement the `LearningPack` SQLAlchemy model in `src/core_database/models.py`.
- [X] T013 Implement the `learning_pack_syllabus` association table in `src/core_database/models.py`.
- [X] T014 Generate a new alembic migration to add the `learning_packs` and association tables.
- [X] T015 Apply the new migration.
- [X] T016 Create a CRUD function `create_learning_pack_with_syllabus()` in `src/core_database/crud.py`.
- [X] T017 Add a test to `tests/test_core_database.py` to verify the creation of a learning pack and its syllabus associations.

## Phase 5: Polish & Cross-Cutting Concerns
- [X] T018 Implement the remaining models from `data-model.md` (`MockExam`, `ExamAttempt`, etc.) in `src/core_database/models.py`.
- [X] T019 Generate and apply the final migration for the remaining tables.
- [X] T020 Add basic CRUD functions for the new models in `src/core_database/crud.py`.
- [X] T021 Add docstrings to all public functions in `crud.py` and `models.py`.
