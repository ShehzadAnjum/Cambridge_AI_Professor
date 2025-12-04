# Tasks: Student-Facing CLI

**Input**: Design documents from `specs/005-student-cli/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Setup
- [X] T001 Create the `src/cli` directory and `__init__.py`.
- [X] T002 Create `src/cli/main.py` with a basic `argparse` setup.
- [X] T003 Create a `pyproject.toml` file to define the project structure and dependencies, and to configure the CLI entry point.

## Phase 2: User Story 1 - Initiate a Learning Loop (Priority: P1)
**Goal**: Allow a student to start a new learning loop for a specific topic via the CLI.
**Independent Test**: The `cambridge-ai-professor start-loop` command successfully triggers the workflow.

### Implementation for User Story 1
- [X] T004 Implement the `start-loop` subcommand in `src/cli/main.py`.
- [X] T005 Integrate the `start-loop` command with the `a_star_workflow_orchestrator.run_full_loop` function.
- [X] T006 Create tests for the CLI in `tests/test_cli.py` to verify that the `start-loop` command works as expected.

## Phase 3: Polish & Cross-Cutting Concerns
- [X] T007 Add comprehensive error handling for invalid arguments and orchestrator failures.
- [X] T008 Add docstrings and type hints to all public functions.
- [X] T009 Create a `README.md` in the `src/cli` directory with instructions on how to use the CLI.
