from app.agents.react_agent import ReactAgent
from app.execution.sandbox_runner import sandbox_runner
from app.core.event_bus import event_bus

from app.memory.memory_manager import memory_manager
from app.safety.action_validator import action_validator


class AgentLoop:

    def __init__(self):

        self.agent = ReactAgent()

    async def run(self, task, session_id):

        context = ""

        memory_manager.store_user_prompt(session_id, task)

        for step in range(20):

            action = self.agent.think(task, session_id, context)

            thought = action.get("thought")
            tool = action.get("action")
            input_data = action.get("input")

            memory_manager.store_agent_message(session_id, thought)

            await event_bus.broadcast({
                "agent": "react-agent",
                "message": thought
            })

            if tool == "none":
                break

            if not action_validator.validate(action):

                await event_bus.broadcast({
                    "agent": "system",
                    "message": "Invalid tool requested"
                })

                break

            result = sandbox_runner.run_tool(tool, input_data)

            await event_bus.broadcast({
                "agent": "tool",
                "message": f"Executed {tool}",
                "data": result
            })

            context += f"\nAction: {tool}\nResult: {result}\n"

        return context


agent_loop = AgentLoop()