from app.llm.ollama_client import ollama_client
from app.llm.prompts import CODE_GENERATOR_PROMPT
from app.core.workflow_logger import WorkflowLogger


class CodeGeneratorAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def generate_code(self, task, plan, language):

        self.logger.log("CodeGeneratorAgent", "Generating code")

        prompt = CODE_GENERATOR_PROMPT.format(task=task, language=language, plan=plan)

        code = ollama_client.generate(prompt)


        self.logger.log("CodeGeneratorAgent", "Code generated")

        return code