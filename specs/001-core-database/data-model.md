# Data Model for Core Database

This document outlines the data entities and their relationships for the A-Level Learning System, as planned in `plan.md`.

## Entity-Relationship Diagram (Conceptual)

```
[Student] 1--* [ExamAttempt]
[MockExam] 1--* [ExamAttempt]
[Student] 1--* [LearningPack]

[Resource] *--* [LearningPack] (many-to-many)
[SyllabusPoint] *--* [LearningPack] (many-to-many)

[ExamAttempt] 1--* [AttemptedQuestion]
[Question] 1--* [AttemptedQuestion]
```

## Entities

### `Student`
Represents a user of the system.
-   `id` (PK)
-   `username` (string, unique)
-   `created_at` (datetime)

### `Resource`
Represents a single educational file.
-   `id` (PK)
-   `subject` (string)
-   `year` (integer)
-   `paper` (integer)
-   `variant` (integer)
-   `type` (string, e.g., 'Past Paper', 'Mark Scheme')
-   `path` (string, unique)
-   `last_seen` (datetime)

### `SyllabusPoint`
A trackable item from a subject's syllabus.
-   `id` (PK)
-   `subject` (string)
-   `code` (string, e.g., '9706/AS/1.1')
-   `description` (text)

### `LearningPack`
A collection of resources for a study session.
-   `id` (PK)
-   `student_id` (FK to Student)
-   `created_at` (datetime)

### `MockExam`
A generated test paper for a student.
-   `id` (PK)
-   `student_id` (FK to Student)
-   `subject` (string)
-   `created_at` (datetime)

### `ExamAttempt`
A student's submission for a mock exam.
-   `id` (PK)
-   `student_id` (FK to Student)
-   `mock_exam_id` (FK to MockExam)
-   `score` (float)
-   `submitted_at` (datetime)

### Association Tables
-   `learning_pack_resources` (learning_pack_id, resource_id)
-   `learning_pack_syllabus` (learning_pack_id, syllabus_point_id)
-   `mock_exam_questions` (mock_exam_id, question_id)
-   `attempted_questions` (exam_attempt_id, question_id, score, diagnosed_weakness)
