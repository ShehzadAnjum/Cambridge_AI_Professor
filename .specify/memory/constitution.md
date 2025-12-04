<!--
Sync Impact Report:
Version change: N/A -> 1.0 (MINOR: New principles added)
Modified principles: None (initial creation)
Added sections: Core Principles (I, II, III, IV), Operational Mandates (Technology & Data, Governance)
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending (Constitution Check section needs review)
  - .specify/templates/spec-template.md: ✅ updated (no direct impact, but general principles apply)
  - .specify/templates/tasks-template.md: ✅ updated (no direct impact, but general principles apply)
Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Clarify if a specific date or "Today" is preferred. Using "2025-12-04" for now.
-->
# A-Level Learning System Constitution

## Core Principles

### I. Dynamic Resource Management
The system will not assume a fixed, static set of local resources. At runtime, it will dynamically scan the local `resource_bank` and pre-approved web repositories for all educational materials (syllabuses, past papers, mark schemes, examiner reports, textbooks, etc.). This ensures the system is always working with the most current and comprehensive set of available information.

### II. On-the-Fly Content Generation
All student-facing content, including "Daily Learning Packs" and mock examinations, will be generated dynamically based on the resources discovered at runtime. This allows for an adaptive workflow that can function even with an incomplete resource set and can incorporate new materials as they become available.

### III. Persistent State Tracking
All system and student activities must be logged to a persistent, structured database. This includes, but is not limited to:
-   **Resource Inventory:** A record of all discovered resources (local and web-based) and their metadata.
-   **Syllabus Coverage:** Tracking which sections of each subject's syllabus have been covered.
-   **Student Progress:** A log of completed tasks, time spent, and concepts studied.
-   **Assessment Data:** Detailed results from all mock exams, including individual question scores, marked papers, and diagnosed areas of weakness.
This data is the foundation for all analysis, reporting, and strategic planning.

### IV. A*-Focused Workflow (NON-NEGOTIABLE)
The system's core operational loop is immutable:
1.  **Assign & Study:** Generate and assign a learning pack based on the strategic plan and available resources.
2.  **Create & Test:** Generate a relevant examination paper (from past papers or custom-built).
3.  **Mark & Diagnose:** Mark the student's attempt against the official mark scheme and use examiner reports to diagnose specific weaknesses and misunderstandings.
4.  **Prescribe & Remediate:** Prescribe a targeted fix for each identified weakness.
5.  **Model & Update:** Provide an A* model answer and update the central strategic plan based on the student's performance data.

## Operational Mandates

### Technology & Data
-   The primary database for state tracking will be a local or cloud-based solution that allows for structured querying.
-   Resource discovery will prioritize local files and fallback to designated web scrapers for approved sources. All downloaded web resources will be cached locally in the appropriate `resource_bank` directory.

### Governance
This Constitution is the supreme operational directive for the A-Level Learning agent. Any proposed deviation or amendment must be explicitly discussed, justified against the A* objective, and ratified by the user before implementation.

**Version**: 1.0 | **Ratified**: 2025-12-04 | **Last Amended**: N/A