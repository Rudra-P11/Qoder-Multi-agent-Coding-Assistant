from fastapi import APIRouter

from app.models.task_models import TaskRequest
from app.core.orchestrator import orchestrator

router = APIRouter()

@router.post("/task")

async def create_task(task: TaskRequest):

    plan = await orchestrator.start_task(task.prompt)

    return {
        "plan": plan
    }