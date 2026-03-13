import json

from app.llm.gemini_client import gemini_client
from app.llm.prompts import REACT_AGENT_PROMPT

from app.memory.context_builder import context_builder


class ReactAgent:

    def think(self, task, session_id, context):

        project_context = context_builder.build_context(session_id)

        prompt = f"""
{REACT_AGENT_PROMPT}

Task:
{task}

Context:
{context}

Project State:
{project_context}

Decide next action.
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