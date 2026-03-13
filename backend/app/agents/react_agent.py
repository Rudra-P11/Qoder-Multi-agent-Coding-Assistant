import json

from app.llm.gemini_client import gemini_client
from app.llm.prompts import REACT_AGENT_PROMPT


class ReactAgent:

    def think(self, task, context):

        prompt = f"""
{REACT_AGENT_PROMPT}

Task:
{task}

Context:
{context}

Decide the next action.
"""

        response = gemini_client.generate(prompt)

        try:

            action = json.loads(response)

        except:

            action = {
                "thought": "Invalid output",
                "action": "none",
                "input": {}
            }

        return action