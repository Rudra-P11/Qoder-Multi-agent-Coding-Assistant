import json

from app.agents.react_agent import ReactAgent
from app.agents.reflection_agent import ReflectionAgent

from app.execution.sandbox_runner import sandbox_runner
from app.core.event_bus import event_bus

from app.memory.memory_manager import memory_manager
from app.safety.action_validator import action_validator


class AgentLoop:

    def __init__(self):

        self.agent = ReactAgent()
        self.reflector = ReflectionAgent()

        self.max_steps = 20

    async def run(self, task, session_id):

        context = ""

        memory_manager.store_user_prompt(session_id, task)

        await event_bus.broadcast({
            "agent": "react-agent",
            "message": "Starting reasoning loop"
        })

        for step in range(self.max_steps):

            action = self.agent.think(task, session_id, context)

            thought = action.get("thought")
            tool = action.get("action")
            input_data = action.get("input")

            memory_manager.store_agent_message(session_id, thought)

            await event_bus.broadcast({
                "agent": "react-agent",
                "message": thought,
                "data": {
                    "step": step
                }
            })

            if tool == "none":

                await event_bus.broadcast({
                    "agent": "react-agent",
                    "message": "Agent finished reasoning"
                })

                break

            if not action_validator.validate(action):

                await event_bus.broadcast({
                    "agent": "system",
                    "message": "Invalid tool requested. Aborting."
                })

                break

            await event_bus.broadcast({
                "agent": "tool",
                "message": f"Executing tool: {tool}",
                "data": input_data
            })

            try:

                result = sandbox_runner.run_tool(tool, input_data)

            except Exception as e:

                result = {
                    "status": "error",
                    "error": str(e)
                }

            await event_bus.broadcast({
                "agent": "tool",
                "message": f"Tool {tool} executed",
                "data": result
            })

            context += f"\nThought: {thought}"
            context += f"\nAction: {tool}"
            context += f"\nResult: {result}\n"

        reflection = self.reflector.reflect(task, context)

        await event_bus.broadcast({
            "agent": "reflection",
            "message": reflection
        })

        return {
            "context": context,
            "reflection": reflection
        }


agent_loop = AgentLoop()