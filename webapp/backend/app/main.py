from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Generator

from . import schemas
from src.core_database.database import SessionLocal
from src.a_star_workflow_orchestrator.orchestrator import run_full_loop

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/start-loop")
def start_learning_loop(request: schemas.StartLoopRequest, db: Session = Depends(get_db)):
    """
    Starts a new A*-Workflow learning loop for a student.
    """
    try:
        print(f"Received request to start loop for student {request.student_id} with topics {request.topics}")
        run_full_loop(
            student_id=request.student_id,
            syllabus_topic_codes=request.topics,
            db=db
        )
        return {"message": "Learning loop started successfully."}
    except Exception as e:
        return {"error": str(e)}
