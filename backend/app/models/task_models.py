from pydantic import BaseModel
from typing import List, Dict, Optional


class TaskRequest(BaseModel):
    prompt: str


class PlanApprovalRequest(BaseModel):
    session_id: str
    approved: bool

class PlanModificationRequest(BaseModel):
    session_id: str
    new_plan: List[str]

class ClarificationResponse(BaseModel):
    session_id: str
    answers: Dict[str, str]  # {"q1": "Python", "q2": "File output"}

class EscalationResponse(BaseModel):
    session_id: str
    choice: str  # "replan" | "simplify" | "pause"