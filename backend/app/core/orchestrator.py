from app.agents.planner_agent import PlannerAgent
from app.execution.agent_loop import agent_loop

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
            "data": {
                "session_id": session_id,
                "task": task
            }
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
            "data": {
                "session_id": session_id,
                "plan": plan
            }
        })

        await event_bus.broadcast({
            "agent": "system",
            "message": "Waiting for user approval"
        })

        return session_id, plan


    async def approve_plan(self, session_id):

        session = session_manager.get_session(session_id)

        if not session:
            return {"error": "Invalid session"}

        task = session["prompt"]

        session_manager.approve_plan(session_id)

        plan = plan_manager.get_plan(session_id)

        todo_manager.create_todo(plan)

        await event_bus.broadcast({
            "agent": "system",
            "message": "Plan approved. TODO created.",
            "data": {
                "plan": plan
            }
        })

        await event_bus.broadcast({
            "agent": "system",
            "message": "Starting agent execution"
        })

        # Brief delay to avoid Gemini free-tier rate limit (5 req/min) after planning
        import asyncio
        await event_bus.broadcast({"agent": "system", "message": "Waiting 12s for rate limit..."})
        await asyncio.sleep(12)

        result = await agent_loop.run(task, session_id)

        await event_bus.broadcast({
            "agent": "system",
            "message": "Execution finished",
            "data": {
                "result": result
            }
        })

        return {
            "status": "completed",
            "result": result
        }

orchestrator = AgentOrchestrator()