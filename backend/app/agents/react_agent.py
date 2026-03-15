import json

from app.llm.ollama_client import ollama_client, repair_json
from app.llm.prompts import REACT_AGENT_PROMPT


class ReactAgent:

    def think(self, task: str, session_id: str, context: str) -> dict:

        # Format context as a clean Action → Observation history block
        history_section = ""
        if context.strip():
            history_section = f"\n=== HISTORY (what you have already done) ===\n{context.strip()}\n=== END HISTORY ===\n"

        prompt = (
            REACT_AGENT_PROMPT
            + f"\nUser task: {task}"
            + history_section
            + "\nYour next JSON action (output ONLY the JSON, nothing else):\n"
        )

        response = ollama_client.generate_json(prompt)

        try:
            # Strip markdown json fences if the model wraps output in them
            cleaned = response.strip()
            # Remove ```json ... ``` wrappers
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            # Try to repair unescaped quotes before parsing
            cleaned = repair_json(cleaned)

            # If model outputs multiple JSON objects, take the first one
            if cleaned.count("{") > 1:
                # Find the end of the first complete object
                depth = 0
                end_idx = 0
                for i, ch in enumerate(cleaned):
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            end_idx = i + 1
                            break
                cleaned = cleaned[:end_idx]

            action = json.loads(cleaned)

        except Exception as e:
            # Log raw output for debugging but don't crash the loop
            action = {
                "thought": f"Failed to parse LLM output as JSON. Raw: {response[:300]} | Error: {e}",
                "action": "none",
                "input": {}
            }

        return action