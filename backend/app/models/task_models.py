from pydantic import BaseModel
from typing import List


class TaskRequest(BaseModel):

    prompt: str


class PlanApprovalRequest(BaseModel):

    session_id: str
    approved: bool

class PlanModificationRequest(BaseModel):

    session_id: str
    new_plan: List[str]