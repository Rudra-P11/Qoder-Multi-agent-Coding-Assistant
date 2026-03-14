from app.llm.gemini_client import gemini_client
from app.core.workflow_logger import WorkflowLogger


class ReflectionAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def reflect(self, code: str, output: str):

        self.logger.log("ReflectionAgent", "Reflecting on result")

        prompt = f"""
Code:
{code}

Output:
{output}

Summarize what happened and whether the task succeeded.
If not successful, suggest improvements or next steps.
"""

        return gemini_client.generate(prompt)


reflection_agent = ReflectionAgent()