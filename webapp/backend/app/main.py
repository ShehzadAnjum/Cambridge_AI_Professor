from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Generator, List, Dict, Any

from . import schemas
from src.core_database.database import SessionLocal
from src.a_star_workflow_orchestrator.orchestrator import LearningLoop

# In a real app, you would manage a dictionary of active loops.
# This is a simple in-memory store for demonstration purposes.
# It will be lost if the server restarts.
active_loops: Dict[int, LearningLoop] = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/loop", response_model=schemas.LoopState)
def start_loop(request: schemas.StartLoopRequest, db: Session = Depends(get_db)):
    """
    Starts a new learning loop, performs the 'assign' stage, and returns the initial state.
    """
    # A simple way to generate a loop ID for this demo
    loop_id = len(active_loops) + 1 
    loop = LearningLoop(student_id=request.student_id, db=db, syllabus_topic_codes=request.topics)
    
    if not loop.assign():
        raise HTTPException(status_code=400, detail="Failed to generate learning pack. Resources may not be available.")

    active_loops[loop_id] = loop
    
    return schemas.LoopState(
        loop_id=loop_id,
        student_id=loop.student_id,
        current_stage=loop.current_stage,
        learning_pack_id=loop.learning_pack.id if loop.learning_pack else None
    )

@app.post("/api/loop/{loop_id}/generate-test", response_model=schemas.ExamDetails)
def generate_test_endpoint(loop_id: int, db: Session = Depends(get_db)):
    """
    Generates a mock exam for the given loop and returns the questions.
    """
    loop = active_loops.get(loop_id)
    if not loop:
        raise HTTPException(status_code=404, detail="Learning loop not found.")
    
    mock_exam = loop.generate_test()
    if not mock_exam:
        raise HTTPException(status_code=400, detail="Failed to generate mock exam. Insufficient questions may be available.")
        
    return schemas.ExamDetails(
        mock_exam_id=mock_exam.id,
        questions=[schemas.Question.model_validate(q) for q in mock_exam.questions]
    )

@app.post("/api/loop/{loop_id}/submit-test", response_model=schemas.ExamResult)
def submit_test_endpoint(loop_id: int, request: schemas.SubmitTestRequest, db: Session = Depends(get_db)):
    """
    Submits user answers, scores the test, and returns the diagnosis.
    """
    loop = active_loops.get(loop_id)
    if not loop:
        raise HTTPException(status_code=404, detail="Learning loop not found.")
        
    # Convert list of answers to dictionary
    answers_dict = {answer.question_id: answer.answer_text for answer in request.answers}
    
    results = loop.submit_and_diagnose(answers_dict)
    if not results:
        raise HTTPException(status_code=500, detail="Failed to process test submission.")
        
    return schemas.ExamResult.model_validate(results)