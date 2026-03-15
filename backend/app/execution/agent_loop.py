import json

from app.agents.react_agent import ReactAgent
from app.agents.reflection_agent import ReflectionAgent

from app.execution.sandbox_runner import sandbox_runner
from app.core.event_bus import event_bus

from app.memory.memory_manager import memory_manager
from app.safety.action_validator import action_validator

from app.agents.supervisor_agent import supervisor_agent
from app.sandbox.workspace_manager import workspace_manager


class AgentLoop:

    def __init__(self):
        self.agent = ReactAgent()
        self.reflector = ReflectionAgent()
        self.max_steps = 10


    async def run(self, task, session_id):
        context = ""
        memory_manager.store_user_prompt(session_id, task)
        
        execution_attempt = 1
        last_action_key = None
        repeat_count = 0

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

            # Deduplication guard: if the agent is calling the same tool with same args twice, force a correction
            try:
                action_key = f"{tool}:{json.dumps(input_data, sort_keys=True)}"
            except Exception:
                action_key = f"{tool}:{str(input_data)}"
            
            if action_key == last_action_key:
                repeat_count += 1
            else:
                repeat_count = 0
                last_action_key = action_key

            if repeat_count >= 2:
                correction_msg = (
                    f"STOP. You have called '{tool}' with the same input {repeat_count + 1} times already. "
                    f"Do NOT call '{tool}' again with the same input. "
                    f"If you wrote a file, call run_code to execute it now. "
                    f"If run_code already succeeded, output action 'none' to finish."
                )
                context += f"\n[LOOP DETECTED] {correction_msg}\n"
                await event_bus.broadcast({"agent": "system", "message": f"[LOOP DETECTED] Repeated call to {tool} blocked. Agent redirected."})
                continue

            # 3. Tool Execution with Self-Correction
            try:
                result = sandbox_runner.run_tool(tool, input_data)
                
                # Check for execution failure based on exit code or explicit status
                if result.get("exit_code") != 0 and result.get("exit_code") is not None:
                    # Treat non-zero exit code as an error to trigger self-correction
                    if "error" not in result:
                        result["error"] = f"Execution failed with exit code {result.get('exit_code')}\nStderr: {result.get('stderr', '')}"
            
            except Exception as e:
                result = {
                    "status": "error",
                    "error": str(e)
                }

            is_error = "error" in result or result.get("status") == "error"

            if tool == "run_code":
                file_path = input_data.get("file_path") or input_data.get("file", "")
                try:
                    code_content = workspace_manager.read_file(file_path) if file_path else "No file path provided."
                except Exception:
                    code_content = "Failed to read code file."
                
                payload_data = {
                    "task": task,
                    "code": code_content,
                    "result": result
                }
                
                if is_error:
                    await event_bus.broadcast({
                        "agent": "execution",
                        "message": f"Attempt {execution_attempt} -> Code Generated -> Execution Error",
                        "data": payload_data
                    })
                    execution_attempt += 1
                else:
                    await event_bus.broadcast({
                        "agent": "execution",
                        "message": f"Attempt {execution_attempt} -> Final Code -> Success",
                        "data": payload_data
                    })
                    execution_attempt += 1
            else:
                if is_error:
                    await event_bus.broadcast({
                        "agent": "debugger",
                        "message": f"Execution failed for tool {tool}. Triggering self-correction...",
                        "data": result
                    })
                else:
                    await event_bus.broadcast({
                        "agent": "tool",
                        "message": f"Tool {tool} execution sequence complete",
                        "data": result
                    })

            if is_error:
                # Inject error into context to help the agent correct itself in the next iteration
                context += f"\n[Self-Correction Triggered] Tool {tool} returned error: {result.get('error') or result}\n"

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