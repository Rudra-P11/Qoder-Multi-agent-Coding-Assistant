from fastapi import APIRouter

from app.models.task_models import (
    TaskRequest,
    PlanApprovalRequest,
    PlanModificationRequest,
    ClarificationResponse,
    EscalationResponse
)

from app.core.orchestrator import orchestrator
from app.core.plan_manager import plan_manager


router = APIRouter()


@router.post("/task")
async def create_task(task: TaskRequest):
    session_id, plan, analysis = await orchestrator.start_task(task.prompt)

    if analysis and analysis.get("needs_clarification"):
        # Return clarification questions — frontend shows ClarificationPanel
        return {
            "session_id": session_id,
            "needs_clarification": True,
            "ambiguity_score": analysis["score"],
            "questions": analysis["questions"],
            "plan": None
        }

    return {
        "session_id": session_id,
        "needs_clarification": False,
        "plan": plan
    }


@router.post("/task/clarify")
async def clarify_task(request: ClarificationResponse):
    """User submitted answers to ambiguity questions — proceed with constrained planning."""
    session_id, plan, _ = await orchestrator.clarify_and_plan(request.session_id, request.answers)
    return {
        "session_id": session_id,
        "plan": plan
    }


@router.post("/task/escalate")
async def escalate_task(request: EscalationResponse):
    """User chose how to handle an agent that's stuck after 3 retries."""
    result = await orchestrator.replan_after_stuck(
        request.session_id,
        stuck_context="",  # agent_loop will store context before escalating
        choice=request.choice
    )
    return result


@router.post("/approve-plan")
async def approve_plan(request: PlanApprovalRequest):
    plan = await orchestrator.approve_plan(request.session_id)
    return {"status": "approved", "plan": plan}


@router.post("/modify-plan")
async def modify_plan(request: PlanModificationRequest):
    new_plan = plan_manager.modify_plan(request.session_id, request.new_plan)
    return {"status": "modified", "plan": new_plan}