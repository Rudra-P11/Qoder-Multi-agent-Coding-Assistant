from app.llm.ollama_client import ollama_client
from app.core.workflow_logger import WorkflowLogger


class CodeGeneratorAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def generate_code(self, task, plan, language):

        self.logger.log("CodeGeneratorAgent", "Generating code")

        prompt = f"""
You are a coding agent.

Task:
{task}

Language:
{language}

Execution Plan:
{plan}

Generate complete working code.

Rules:
- Only output code
- No explanations
"""

        code = ollama_client.generate(prompt)

        self.logger.log("CodeGeneratorAgent", "Code generated")

        return code