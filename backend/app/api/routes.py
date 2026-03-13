from fastapi import APIRouter

from app.models.task_models import (
    TaskRequest,
    PlanApprovalRequest,
    PlanModificationRequest
)

from app.core.orchestrator import orchestrator
from app.core.plan_manager import plan_manager


router = APIRouter()


@router.post("/task")

async def create_task(task: TaskRequest):

    session_id, plan = await orchestrator.start_task(task.prompt)

    return {
        "session_id": session_id,
        "plan": plan
    }

@router.post("/approve-plan")

async def approve_plan(request: PlanApprovalRequest):

    plan = await orchestrator.approve_plan(request.session_id)

    return {
        "status": "approved",
        "plan": plan
    }


@router.post("/modify-plan")

async def modify_plan(request: PlanModificationRequest):

    new_plan = plan_manager.modify_plan(
        request.session_id,
        request.new_plan
    )

    return {
        "status": "modified",
        "plan": new_plan
    }