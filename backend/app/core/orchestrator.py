from app.agents.planner_agent import PlannerAgent
from app.core.event_bus import event_bus
from app.core.session_manager import session_manager
from app.core.plan_manager import plan_manager
from app.project.todo_manager import todo_manager


class AgentOrchestrator:

    def __init__(self):

        self.planner = PlannerAgent()

    async def start_task(self, task: str):

        session_id = session_manager.create_session(task)

        await event_bus.broadcast({
            "agent": "system",
            "message": "Task received",
            "data": {"session_id": session_id}
        })

        await event_bus.broadcast({
            "agent": "planner",
            "message": "Planning task"
        })

        plan = self.planner.create_plan(task)

        plan_manager.store_plan(session_id, plan)

        await event_bus.broadcast({
            "agent": "planner",
            "message": "Plan generated",
            "data": {"plan": plan, "session_id": session_id}
        })

        await event_bus.broadcast({
            "agent": "system",
            "message": "Waiting for user approval"
        })

        return session_id, plan

    async def approve_plan(self, session_id):

        session_manager.approve_plan(session_id)

        plan = plan_manager.get_plan(session_id)

        todo_manager.create_todo(plan)

        await event_bus.broadcast({
            "agent": "system",
            "message": "Plan approved. TODO file created.",
            "data": {"plan": plan}
        })

        return plan

orchestrator = AgentOrchestrator()