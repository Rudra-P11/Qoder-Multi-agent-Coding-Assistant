from app.llm.gemini_client import gemini_client
from app.core.workflow_logger import WorkflowLogger


class CoderAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def generate_code(self, task: str, plan: list):

        self.logger.log("CoderAgent", "Generating code")

        plan_text = "\n".join(plan)

        prompt = f"""
You are a coding agent.

Task:
{task}

Plan:
{plan_text}

Write the complete working code.
"""

        code = gemini_client.generate(prompt)

        self.logger.log("CoderAgent", "Code generated")

        return code


coder_agent = CoderAgent()