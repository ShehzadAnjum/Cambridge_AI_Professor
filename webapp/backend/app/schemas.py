from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Request Models ---

class StartLoopRequest(BaseModel):
    student_id: int
    topics: List[str]

class Answer(BaseModel):
    question_id: int
    answer_text: str

class SubmitTestRequest(BaseModel):
    answers: List[Answer]

# --- Response Models ---

class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_number: str
    # The actual text would be retrieved separately if needed, to keep this payload small
    # For now, we assume the frontend doesn't need to display the full text again.
    max_marks: Optional[int] = None

class ExamDetails(BaseModel):
    mock_exam_id: int
    questions: List[Question]

class DiagnosedWeakness(BaseModel):
    question_number: str
    weakness: str
    suggestion: str

class ExamResult(BaseModel):
    total_score: float
    max_score: float
    weaknesses: List[DiagnosedWeakness]

class LoopState(BaseModel):
    loop_id: int
    student_id: int
    current_stage: str
    learning_pack_id: Optional[int] = None
    mock_exam_id: Optional[int] = None
    exam_result: Optional[ExamResult] = None