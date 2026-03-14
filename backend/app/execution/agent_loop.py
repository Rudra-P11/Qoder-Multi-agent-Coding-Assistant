import json

from app.agents.react_agent import ReactAgent
from app.agents.reflection_agent import ReflectionAgent

from app.execution.sandbox_runner import sandbox_runner
from app.core.event_bus import event_bus

from app.memory.memory_manager import memory_manager
from app.safety.action_validator import action_validator

from app.agents.supervisor_agent import supervisor_agent


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
            # 1. ReAct Reasoning Step
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

            # Check if agent is finished
            if tool == "none":
                await event_bus.broadcast({
                    "agent": "react-agent",
                    "message": "Agent finished reasoning"
                })
                break

            # 2. Safety Validation
            if not action_validator.validate(action):
                await event_bus.broadcast({
                    "agent": "system",
                    "message": f"Invalid tool '{tool}' requested. Aborting."
                })
                break

            await event_bus.broadcast({
                "agent": "tool",
                "message": f"Executing tool: {tool}",
                "data": input_data
            })

            # 3. Tool Execution with Self-Correction (Retries)
            max_retries = 3
            attempt = 0
            result = None

            while attempt < max_retries:
                try:
                    result = sandbox_runner.run_tool(tool, input_data)
                    
                    # If execution was successful (exit_code 0), break retry loop
                    if result.get("exit_code") == 0 or result.get("status") == "success":
                        break
                
                except Exception as e:
                    result = {
                        "status": "error",
                        "error": str(e)
                    }

                attempt += 1
                
                # Feedback loop: Broadcast retry and update context so the agent sees the error
                await event_bus.broadcast({
                    "agent": "debugger",
                    "message": f"Retry attempt {attempt} for tool: {tool}",
                    "data": result
                })

                # Inject error into context to help the agent correct itself in the next iteration
                context += f"\n[Attempt {attempt}] Error: {result.get('error') or result}\n"
                
                # Note: In a true self-correction loop, you might call self.agent.think() 
                # again here to get NEW input_data based on the error. 
                # As written, it retries the same input_data.

            await event_bus.broadcast({
                "agent": "tool",
                "message": f"Tool {tool} execution sequence complete",
                "data": result
            })

            # Update context for the next step in the main loop
            context += f"\nThought: {thought}"
            context += f"\nAction: {tool}"
            context += f"\nResult: {result}\n"

        # 4. Final Reflection and Supervision
        reflection = self.reflector.reflect(task, context)

        await event_bus.broadcast({
            "agent": "reflection",
            "message": reflection
        })

        supervisor_advice = supervisor_agent.evaluate(task, context)

        await event_bus.broadcast({
            "agent": "supervisor",
            "message": supervisor_advice
        })

        return {
            "context": context,
            "reflection": reflection,
            "supervisor_advice": supervisor_advice
        }


agent_loop = AgentLoop()