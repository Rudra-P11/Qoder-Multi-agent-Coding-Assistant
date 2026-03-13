from pydantic import BaseModel
from typing import List


class TaskRequest(BaseModel):

    prompt: str


class PlanResponse(BaseModel):

    steps: List[str]


class AgentEvent(BaseModel):

    agent: str
    message: str
    data: dict | None = None