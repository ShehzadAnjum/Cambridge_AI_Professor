# Cambridge AI Professor CLI

This CLI is the main entry point for students to interact with the A-Level Learning System.

## Installation

To install the CLI and its dependencies, run the following command from the project root:

```bash
pip install .
```

## Usage

### Start a Learning Loop

To start a new learning loop for a student, use the `start-loop` command:

```bash
cambridge-ai-professor start-loop --student-id <student_id> --topics <topic_code_1> <topic_code_2> ...
```

**Arguments:**

-   `--student-id`: The ID of the student.
-   `--topics`: A space-separated list of syllabus topic codes to focus on.

**Example:**

```bash
cambridge-ai-professor start-loop --student-id 1 --topics 1.1 1.2
```
