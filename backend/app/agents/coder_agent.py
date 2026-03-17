from app.llm.gemini_client import gemini_client
from app.llm.prompts import CODER_AGENT_PROMPT
from app.core.workflow_logger import WorkflowLogger


class CoderAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def generate_code(self, task: str, plan: list):

        self.logger.log("CoderAgent", "Generating code")

        plan_text = "\n".join(plan)

        prompt = CODER_AGENT_PROMPT.format(task=task, plan_text=plan_text)

        code = gemini_client.generate(prompt)


        self.logger.log("CoderAgent", "Code generated")

        return code


coder_agent = CoderAgent()