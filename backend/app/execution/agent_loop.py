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


    async def run(self, task: str, session_id: str, plan: list = None):
        import os
        from app.tools.read_todo import read_todo

        context_parts = []

        # 1. Inject the TODO file content (authoritative source of steps + filenames)
        todo_content = read_todo()
        if todo_content:
            context_parts.append(
                f"=== YOUR TODO LIST (follow this exactly, use the exact filenames listed) ===\n"
                f"{todo_content}\n"
                f"=== END TODO ==="
            )

        # 2. List existing workspace files so agent knows what's already there
        try:
            existing_files = workspace_manager.list_files()
            if existing_files:
                files_str = "\n".join(f"  - {f}" for f in existing_files)
                context_parts.append(f"=== EXISTING WORKSPACE FILES ===\n{files_str}\n=== END FILES ===")
        except Exception:
            pass

        context = "\n\n".join(context_parts)
        memory_manager.store_user_prompt(session_id, task)

        
        execution_attempt = 1
        last_action_key = None
        repeat_count = 0
        last_written_file = None  # Track the most recently written file path


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

            # Don't log file content to terminal — it belongs in the editor, not the log
            log_data = (
                {"path": input_data.get("path")}
                if tool in ("write_file", "append_file")
                else input_data
            )
            await event_bus.broadcast({
                "agent": "tool",
                "message": f"Executing tool: {tool}",
                "data": log_data
            })

            # ── Deduplication / forced-progression guard ────────────────────
            # For write_file: key on (tool + path) only — NOT content.
            # The model often generates slightly different content each call,
            # so keying on full input_data would miss successive writes to the same file.
            try:
                if tool == "write_file":
                    action_key = f"write_file:{input_data.get('path', '')}"
                else:
                    action_key = f"{tool}:{json.dumps(input_data, sort_keys=True)}"
            except Exception:
                action_key = f"{tool}:{str(input_data)}"

            if action_key == last_action_key:
                repeat_count += 1
            else:
                repeat_count = 0
                last_action_key = action_key

            if repeat_count >= 2:
                if tool == "write_file":
                    # FORCED PROGRESSION: auto-run the file instead of warning the LLM
                    written_path = input_data.get("path", "") or last_written_file or ""
                    if written_path:
                        await event_bus.broadcast({
                            "agent": "system",
                            "message": f"[AUTO] write_file loop detected. Forcing run_code on: {written_path}"
                        })
                        # Override tool and input — fall through to execution
                        tool = "run_code"
                        input_data = {"file_path": written_path}
                        repeat_count = 0
                        last_action_key = None
                        # Do NOT continue — let execution proceed below
                    else:
                        await event_bus.broadcast({"agent": "system", "message": "[LOOP] write_file repeated but no path found. Skipping."})
                        continue
                else:
                    await event_bus.broadcast({"agent": "system", "message": f"[LOOP] {tool} repeated {repeat_count + 1}x. Skipping."})
                    context += f"\n[LOOP DETECTED] Stop calling '{tool}'. Move to the next logical step.\n"
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

            # Track the last file successfully written so forced-run fallback can use it
            if tool == "write_file" and not is_error:
                last_written_file = input_data.get("path") or last_written_file

            if tool == "run_code":
                file_path = input_data.get("file_path") or input_data.get("file", "")
                # Show only file metadata — full code is already visible in the editor
                try:
                    code_lines = len(workspace_manager.read_file(file_path).splitlines()) if file_path else 0
                    code_summary = f"{file_path} ({code_lines} lines)"
                except Exception:
                    code_summary = file_path or "unknown file"

                payload_data = {
                    "task": task,
                    "code": code_summary,
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
                # Inject error into context to help the agent correct itself
                context += f"\n[Self-Correction Triggered] Tool {tool} returned error: {result.get('error') or result}\n"

                # ── Dead-end escalation: 3 failed run_code attempts ──────────
                if tool == "run_code" and execution_attempt > 3:
                    await event_bus.broadcast({
                        "agent": "escalation",
                        "message": "Agent is stuck after 3 failed attempts",
                        "data": {
                            "session_id": session_id,
                            "attempts": execution_attempt - 1,
                            "last_error": result.get("error") or result.get("stderr") or "Unknown error",
                            "context_summary": context[-800:]  # last 800 chars of context
                        }
                    })
                    break  # Pause the loop — user will respond via /task/escalate

            # Update context for the next step in the main loop
            context += f"\nThought: {thought}"
            context += f"\nAction: {tool}"
            context += f"\nObservation: {result}\n"

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