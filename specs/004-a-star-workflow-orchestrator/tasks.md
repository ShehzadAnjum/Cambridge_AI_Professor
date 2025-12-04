# Tasks: A*-Workflow Orchestrator

**Input**: Design documents from `specs/004-a-star-workflow-orchestrator/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Setup
- [X] T001 Create the `src/a_star_workflow_orchestrator` directory and `__init__.py`.
- [X] T002 Create `src/a_star_workflow_orchestrator/orchestrator.py`.

## Phase 2: Foundational (Workflow State Management)
- [X] T003 Implement a `LearningLoop` class in `src/a_star_workflow_orchestrator/orchestrator.py` to manage the state of the workflow (e.g., current stage, student_id, topic).
- [X] T004 Implement the `assign()` method in the `LearningLoop` class. This method should call the `content_generation_engine.learning_pack_generator` to create a learning pack and store its ID.

## Phase 3: User Story 1 - Execute a Full Learning Loop (Priority: P1)
**Goal**: Execute all five stages of the learning loop (Assign, Test, Diagnose, Remediate, Model) for a given topic and student.
**Independent Test**: The system can successfully run a full learning loop, with simulated stages for Diagnose, Remediate, and Model.

### Implementation for User Story 1
- [X] T005 Implement the `test()` method in the `LearningLoop` class. This method should call the `content_generation_engine.exam_generator` to create a mock exam and (for now) simulate a student taking the test by creating an `ExamAttempt` with random scores.
- [X] T006 Implement the `diagnose()` method (simulation). This method should analyze the `ExamAttempt` and print a list of "diagnosed weaknesses" to the console.
- [X] T007 Implement the `remediate()` method (simulation). This method should print a "remediation plan" to the console.
- [X] T008 Implement the `model()` method (simulation). This method should print a link to a "model answer" to the console.
- [X] T009 Implement the `run_full_loop()` function in `src/a_star_workflow_orchestrator/orchestrator.py` that calls the five stage methods in sequence.
- [X] T010 Create tests for the `LearningLoop` class in `tests/test_orchestrator.py`.

## Phase 4: Polish & Cross-Cutting Concerns
- [X] T011 Create `src/a_star_workflow_orchestrator/main.py` and implement CLI commands (`start-loop`, `resume-loop`) to interact with the `LearningLoop`.
- [X] T012 Add comprehensive error handling and logging to the orchestrator.
- [X] T013 Add docstrings and type hints to all public functions.
