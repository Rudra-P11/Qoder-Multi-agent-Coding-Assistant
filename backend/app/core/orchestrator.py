from app.agents.planner_agent import PlannerAgent
from app.agents.ambiguity_analyzer import ambiguity_analyzer
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

        await event_bus.broadcast({"agent": "system", "message": "Task received", "data": {"session_id": session_id, "task": task}})

        # ── Ambiguity check ──────────────────────────────────────────────────
        await event_bus.broadcast({"agent": "ambiguity", "message": "Analyzing task clarity..."})

        analysis = ambiguity_analyzer.analyze(task)

        if analysis["needs_clarification"]:
            # Surface questions to user before planning
            await event_bus.broadcast({
                "agent": "ambiguity",
                "message": "Task needs clarification",
                "data": {
                    "session_id": session_id,
                    "score": analysis["score"],
                    "questions": analysis["questions"]
                }
            })
            # Return early — frontend will POST to /task/clarify when user answers
            return session_id, None, analysis

        # ── Planning ─────────────────────────────────────────────────────────
        return await self._plan_and_return(task, session_id)

    async def _plan_and_return(self, task: str, session_id: str, constraints: dict = None):
        """Run the planner and return (session_id, plan, None)."""
        await event_bus.broadcast({"agent": "planner", "message": "Planning task"})

        # Inject clarification constraints into the task prompt if provided
        enriched_task = task
        if constraints:
            constraint_lines = "\n".join(f"- {k}: {v}" for k, v in constraints.items())
            enriched_task = f"{task}\n\nCONSTRAINTS (must follow):\n{constraint_lines}"

        plan = self.planner.create_plan(enriched_task)
        plan_manager.store_plan(session_id, plan)

        await event_bus.broadcast({"agent": "planner", "message": "Plan generated", "data": {"session_id": session_id, "plan": plan}})
        await event_bus.broadcast({"agent": "system", "message": "Waiting for user approval"})

        return session_id, plan, None

    async def clarify_and_plan(self, session_id: str, answers: dict):
        """Called after user fills in the clarification form. Builds constraints and plans."""
        session = session_manager.get_session(session_id)
        if not session:
            return {"error": "Invalid session"}

        task = session["prompt"]

        await event_bus.broadcast({
            "agent": "ambiguity",
            "message": "Clarification received. Planning with constraints.",
            "data": {"answers": answers}
        })

        # answers is {"q1": "Python", "q2": "CLI output", ...}
        # Build human-readable constraints
        constraints = {f"User specified": v for v in answers.values() if v and v != "Agent decides"}

        return await self._plan_and_return(task, session_id, constraints)

    async def approve_plan(self, session_id):
        session = session_manager.get_session(session_id)
        if not session:
            return {"error": "Invalid session"}

        task = session["prompt"]
        session_manager.approve_plan(session_id)
        plan = plan_manager.get_plan(session_id)
        todo_manager.create_todo(plan)

        await event_bus.broadcast({"agent": "system", "message": "Plan approved. TODO created.", "data": {"plan": plan}})
        await event_bus.broadcast({"agent": "system", "message": "Starting agent execution"})

        import asyncio
        await asyncio.sleep(1)

        result = await agent_loop.run(task, session_id, plan=plan)

        await event_bus.broadcast({"agent": "system", "message": "Execution finished", "data": {"result": result}})

        return {"status": "completed", "result": result}

    async def replan_after_stuck(self, session_id: str, stuck_context: str, choice: str):
        """Handle escalation when agent is stuck after 3 retries."""
        session = session_manager.get_session(session_id)
        if not session:
            return {"error": "Invalid session"}

        task = session["prompt"]

        if choice == "replan":
            error_hint = f"Previous attempt failed. Try a completely different approach.\nFailed context: {stuck_context[-500:]}"
            plan = self.planner.create_plan(f"{task}\n\nNOTE: {error_hint}")
            plan_manager.store_plan(session_id, plan)
            todo_manager.create_todo(plan)
            await event_bus.broadcast({"agent": "system", "message": "Replanning with new strategy...", "data": {"plan": plan}})
            result = await agent_loop.run(task, session_id, plan=plan)
            return {"status": "replanned", "result": result}

        elif choice == "simplify":
            simplified = f"Simplest possible version of: {task}"
            plan = self.planner.create_plan(simplified)
            plan_manager.store_plan(session_id, plan)
            todo_manager.create_todo(plan)
            await event_bus.broadcast({"agent": "system", "message": "Simplified task. Replanning...", "data": {"plan": plan}})
            result = await agent_loop.run(simplified, session_id, plan=plan)
            return {"status": "simplified", "result": result}

        else:  # pause
            await event_bus.broadcast({"agent": "system", "message": "Execution paused. Awaiting user guidance."})
            return {"status": "paused"}


orchestrator = AgentOrchestrator()