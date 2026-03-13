from app.agents.planner_agent import PlannerAgent
from app.core.event_bus import event_bus


class AgentOrchestrator:

    def __init__(self):

        self.planner = PlannerAgent()

    async def start_task(self, task: str):

        await event_bus.broadcast({
            "agent": "system",
            "message": "Task received",
            "data": {"task": task}
        })

        await event_bus.broadcast({
            "agent": "planner",
            "message": "Planning task"
        })

        plan = self.planner.create_plan(task)

        await event_bus.broadcast({
            "agent": "planner",
            "message": "Plan generated",
            "data": {"plan": plan}
        })

        return plan

orchestrator = AgentOrchestrator()