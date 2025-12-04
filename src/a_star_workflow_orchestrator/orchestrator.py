from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from src.core_database import crud, models
from src.content_generation_engine import learning_pack_generator, exam_generator
import random
import sys

class LearningLoop:
    """
    Manages the state and execution of the A*-Workflow learning loop across multiple API calls.
    """
    def __init__(self, student_id: int, db: Session, syllabus_topic_codes: List[str] = None):
        self.student_id = student_id
        self.db = db
        self.syllabus_topic_codes = syllabus_topic_codes
        self.current_stage = "start"
        self.learning_pack: Optional[models.LearningPack] = None
        self.mock_exam: Optional[models.MockExam] = None
        self.exam_attempt: Optional[models.ExamAttempt] = None
        # In a real application, this state would be persisted, e.g., in Redis or the DB
        # For this example, we'll rely on keeping the orchestrator instance in memory (not scalable)
        # or refetching from the DB based on a loop_id.

    def assign(self) -> bool:
        print("--- Stage: Assign ---")
        self.learning_pack = learning_pack_generator.generate_learning_pack(
            student_id=self.student_id,
            syllabus_topic_codes=self.syllabus_topic_codes,
            db=self.db
        )
        if self.learning_pack:
            print(f"Generated learning pack ID: {self.learning_pack.id}")
            self.current_stage = "assigned"
            return True
        print("Failed to generate learning pack.", file=sys.stderr)
        return False

    def generate_test(self, num_questions: int = 2) -> Optional[models.MockExam]:
        if self.current_stage != "assigned":
            print("Cannot generate test: assign stage not completed.", file=sys.stderr)
            return None
            
        print("--- Stage: Test ---")
        subject_code = self.learning_pack.syllabus_points[0].subject
        self.mock_exam = exam_generator.generate_mock_exam(
            student_id=self.student_id,
            subject=subject_code,
            num_questions=num_questions,
            db=self.db
        )
        if self.mock_exam:
            print(f"Generated mock exam ID: {self.mock_exam.id}")
            self.current_stage = "test_generated"
            return self.mock_exam
        print("Failed to generate mock exam.", file=sys.stderr)
        return None

    def submit_and_diagnose(self, answers: Dict[int, str]) -> Optional[Dict[str, Any]]:
        if self.current_stage != "test_generated":
            print("Cannot submit test: test not generated.", file=sys.stderr)
            return None
        
        print("--- Stage: Diagnose ---")
        # 1. Create the exam attempt
        self.exam_attempt = models.ExamAttempt(
            student_id=self.student_id,
            mock_exam_id=self.mock_exam.id,
            score=0
        )
        self.db.add(self.exam_attempt)
        self.db.commit()
        self.db.refresh(self.exam_attempt)

        # 2. Simulate scoring and create AttemptedQuestion records
        total_score = 0
        max_total_score = 0
        diagnosed_weaknesses = []

        for question in self.mock_exam.questions:
            max_marks = question.max_marks or 10 # Default marks if not set
            max_total_score += max_marks
            # Simulate scoring based on answer length (dummy logic)
            user_answer = answers.get(question.id, "")
            score = random.uniform(0, max_marks) if len(user_answer) > 5 else 0
            
            attempted_question = models.AttemptedQuestion(
                exam_attempt_id=self.exam_attempt.id,
                question_id=question.id,
                score=score
            )
            if score < (max_marks / 2):
                attempted_question.diagnosed_weakness = "Score is less than 50%. Review topic."
                diagnosed_weaknesses.append({
                    "question_number": question.question_number,
                    "weakness": "Low score",
                    "suggestion": "Review the mark scheme and related resources for this topic."
                })

            self.db.add(attempted_question)
            total_score += score
        
        self.exam_attempt.score = total_score
        self.db.commit()
        
        print(f"Simulated exam submission. Total score: {total_score}/{max_total_score}")
        self.current_stage = "diagnosed"

        return {
            "total_score": total_score,
            "max_score": max_total_score,
            "weaknesses": diagnosed_weaknesses
        }
