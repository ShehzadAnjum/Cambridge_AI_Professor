# Feature Specification: A*-Workflow Orchestrator

**Feature Branch**: `004-a-star-workflow-orchestrator`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "Develop the A*-Workflow orchestrator to manage the learning loop (Assign, Test, Diagnose, Remediate, Model) as per Constitution Principle IV."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Execute a Full Learning Loop (Priority: P1)
As a student, I want to initiate a full learning loop for a specific topic, so that I can be assigned study material, take a test, get my results, and receive a targeted remediation plan.

**Why this priority**: This is the core functionality of the entire system, directly implementing the A*-Focused Workflow.
**Independent Test**: The system can successfully execute all five stages of the learning loop (Assign, Test, Diagnose, Remediate, Model) for a given topic and student.

**Acceptance Scenarios**:
1.  **Given** a student and a syllabus topic are selected, **When** the `start-loop` command is executed, **Then** the system:
    a.  Generates and assigns a `LearningPack`.
    b.  Generates and administers a `MockExam`.
    c.  (Simulates) Marks the exam and diagnoses weaknesses, creating an `ExamAttempt` with scores.
    d.  (Simulates) Generates and presents a remediation plan (e.g., list of weak areas).
    e.  (Simulates) Provides a link to a model answer or relevant resource.
2.  **Given** the system is in the middle of a learning loop (e.g., after a test is completed), **When** the `resume-loop` command is executed, **Then** the system continues from the last completed stage (e.g., proceeds to the Diagnose stage).

## Requirements *(mandatory)*

### Functional Requirements
-   **FR-001**: The system MUST provide a CLI to initiate a new learning loop (`start-loop`) for a student and a set of syllabus topics.
-   **FR-002**: The system MUST provide a CLI to resume an in-progress learning loop (`resume-loop`).
-   **FR-003**: The orchestrator MUST call the `ContentGenerationEngine` to generate learning packs and mock exams.
-   **FR-004**: The orchestrator MUST create and update records in the core database at each stage of the loop (e.g., creating `LearningPack`, `MockExam`, and `ExamAttempt` records).
-   **FR-005**: The system MUST implement the five stages of the A*-Focused Workflow in the correct sequence: Assign, Test, Diagnose, Remediate, Model.
-   **FR-006**: The "Diagnose" stage MUST (initially, can be a simulation) analyze the `ExamAttempt` to identify questions with low scores and record them as diagnosed weaknesses.
-   **FR-007**: The "Remediate" stage MUST (initially, can be a simulation) suggest further study or resources based on the diagnosed weaknesses.
-   **FR-008**: The "Model" stage MUST (initially, can be a simulation) provide a reference to an A* model answer (e.g., the mark scheme for the question).

### Key Entities
-   **WorkflowOrchestrator**: The main component that manages the state of the learning loop.
-   **LearningLoopState**: An object or database entry that tracks the current stage of a learning loop for a student.

## Success Criteria *(mandatory)*

### Measurable Outcomes
-   **SC-001**: A full learning loop can be initiated and completed via the CLI without errors.
-   **SC-002**: After a full loop, the database correctly contains all associated artifacts: a `LearningPack`, a `MockExam`, and an `ExamAttempt` with scores, all linked to the correct student.
-   **SC-003**: Each stage of the workflow (Assign, Test, etc.) is logged to the console, providing clear feedback to the user on the system's progress.