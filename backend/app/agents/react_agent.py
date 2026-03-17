import json

from app.llm.gemini_client import gemini_client
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
            + "\nYour next JSON action:\n"
        )

        # Use the specialized JSON generation method for Gemini
        response = gemini_client.generate_json(prompt)

        try:
            # Gemini's generate_json returns clean JSON without fences
            action = json.loads(response.strip())

        except Exception as e:
            # Log raw output for debugging but don't crash the loop
            action = {
                "thought": f"Failed to parse LLM output as JSON. Raw: {response[:300]} | Error: {e}",
                "action": "none",
                "input": {}
            }

        return action