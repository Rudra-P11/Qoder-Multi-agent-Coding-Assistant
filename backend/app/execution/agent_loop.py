from app.agents.react_agent import ReactAgent
from app.execution.sandbox_runner import sandbox_runner
from app.core.event_bus import event_bus


class AgentLoop:

    def __init__(self):

        self.agent = ReactAgent()

    async def run(self, task):

        context = ""

        for step in range(20):

            action = self.agent.think(task, context)

            thought = action["thought"]
            tool = action["action"]
            input_data = action["input"]

            await event_bus.broadcast({
                "agent": "react-agent",
                "message": thought
            })

            if tool == "none":
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