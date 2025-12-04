from pydantic import BaseModel
from typing import List

class StartLoopRequest(BaseModel):
    student_id: int
    topics: List[str]
