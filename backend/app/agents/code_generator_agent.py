from app.llm.prompts import CODE_SYSTEM_PROMPT
from app.llm.gemini_client import gemini_client
from app.core.workflow_logger import WorkflowLogger


class CodeGeneratorAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def generate_code(self, task, plan):

        self.logger.log("CodeGeneratorAgent", "Generating code")

        prompt = f"""
{CODE_SYSTEM_PROMPT}

Task:
{task}

Plan:
{plan}

Generate the full script.
"""

        code = gemini_client.generate(prompt)

        self.logger.log("CodeGeneratorAgent", "Code generated")

        return code