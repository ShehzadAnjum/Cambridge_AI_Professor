from typing import List, Optional
from sqlalchemy.orm import Session
from src.core_database import crud, models
from src.content_generation_engine import learning_pack_generator, exam_generator
import random
import sys

class LearningLoop:
    """
    Manages the state and execution of the A*-Workflow learning loop.
    """
    def __init__(self, student_id: int, db: Session, syllabus_topic_codes: List[str]) -> None:
        """
        Initializes the LearningLoop with student ID, database session, and syllabus topics.
        """
        self.student_id = student_id
        self.db = db
        self.syllabus_topic_codes = syllabus_topic_codes
        self.current_stage = "start"
        self.learning_pack: Optional[models.LearningPack] = None
        self.mock_exam: Optional[models.MockExam] = None
        self.exam_attempt: Optional[models.ExamAttempt] = None

    def assign(self) -> bool:
        """
        Assign stage: Generates and assigns a learning pack.
        """
        print("--- Stage: Assign ---")
        try:
            self.learning_pack = learning_pack_generator.generate_learning_pack(
                student_id=self.student_id,
                syllabus_topic_codes=self.syllabus_topic_codes,
                db=self.db
            )
            if self.learning_pack:
                print(f"Generated learning pack ID: {self.learning_pack.id}")
                self.current_stage = "assign_complete"
                return True
            else:
                print("Failed to generate learning pack.", file=sys.stderr)
                return False
        except Exception as e:
            print(f"An error occurred during the assign stage: {e}", file=sys.stderr)
            return False

    def test(self) -> bool:
        """
        Test stage: Generates a mock exam and simulates a student attempt.
        """
        if not self.learning_pack:
            print("Cannot start test stage: Learning pack not assigned.", file=sys.stderr)
            return False

        print("--- Stage: Test ---")
        try:
            subject = self.learning_pack.syllabus_points[0].subject
            self.mock_exam = exam_generator.generate_mock_exam(
                student_id=self.student_id,
                subject=subject,
                num_questions=1, # Reduced for simplicity
                db=self.db
            )

            if self.mock_exam:
                print(f"Generated mock exam ID: {self.mock_exam.id}")
                # Simulate taking the test
                self.exam_attempt = models.ExamAttempt(
                    student_id=self.student_id,
                    mock_exam_id=self.mock_exam.id,
                    score=0 # Initial score
                )
                self.db.add(self.exam_attempt)
                self.db.commit()
                self.db.refresh(self.exam_attempt)

                total_score = 0
                if self.mock_exam.questions:
                    for question in self.mock_exam.questions:
                        score = random.uniform(0, question.max_marks)
                        attempted_question = models.AttemptedQuestion(
                            exam_attempt_id=self.exam_attempt.id,
                            question_id=question.id,
                            score=score
                        )
                        self.db.add(attempted_question)
                        total_score += score
                
                self.exam_attempt.score = total_score
                self.db.commit()
                print(f"Simulated exam attempt. Total score: {total_score}")
                self.current_stage = "test_complete"
                return True
            else:
                print("Failed to generate mock exam.", file=sys.stderr)
                return False
        except Exception as e:
            print(f"An error occurred during the test stage: {e}", file=sys.stderr)
            return False

    def diagnose(self) -> bool:
        """
        Diagnose stage: Analyzes the exam attempt to identify weaknesses.
        (Simulation)
        """
        if not self.exam_attempt:
            print("Cannot start diagnose stage: Exam not attempted.", file=sys.stderr)
            return False

        print("--- Stage: Diagnose ---")
        try:
            weaknesses = []
            if self.exam_attempt.attempted_questions:
                for attempted_question in self.exam_attempt.attempted_questions:
                    if attempted_question.question and attempted_question.score < (attempted_question.question.max_marks / 2):
                        weaknesses.append(attempted_question.question)

            if weaknesses:
                print("Diagnosed weaknesses in the following questions:")
                for q in weaknesses:
                    print(f" - Question {q.question_number} (Resource ID: {q.resource_id})")
            else:
                print("No significant weaknesses diagnosed.")
                
            self.current_stage = "diagnose_complete"
            return True
        except Exception as e:
            print(f"An error occurred during the diagnose stage: {e}", file=sys.stderr)
            return False

    def remediate(self) -> bool:
        """
        Remediate stage: Generates a remediation plan.
        (Simulation)
        """
        if self.current_stage != "diagnose_complete":
            print("Cannot start remediate stage: Diagnosis not complete.", file=sys.stderr)
            return False
            
        print("--- Stage: Remediate ---")
        print("Generating remediation plan...")
        print("Recommendation: Review the mark schemes for the questions identified as weaknesses.")
        self.current_stage = "remediate_complete"
        return True

    def model(self) -> bool:
        """
        Model stage: Provides a link to a model answer.
        (Simulation)
        """
        if self.current_stage != "remediate_complete":
            print("Cannot start model stage: Remediation not complete.", file=sys.stderr)
            return False

        print("--- Stage: Model ---")
        print("Providing model answer...")
        print("Model Answer: Please find the mark scheme for the attempted exam in the resource bank.")
        self.current_stage = "model_complete"
        return True
    
    def run(self) -> None:
        """
        Runs the full learning loop.
        """
        if self.assign():
            if self.test():
                if self.diagnose():
                    if self.remediate():
                        self.model()

def run_full_loop(student_id: int, syllabus_topic_codes: List[str], db: Session) -> None:
    """
    Runs a full A*-Workflow learning loop for a student and a set of topics.

    Args:
        student_id: The ID of the student.
        syllabus_topic_codes: A list of syllabus topic codes.
        db: The database session.
    """
    loop = LearningLoop(student_id=student_id, db=db, syllabus_topic_codes=syllabus_topic_codes)
    loop.run()