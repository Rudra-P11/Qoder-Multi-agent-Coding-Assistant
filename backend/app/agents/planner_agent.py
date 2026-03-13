from app.llm.prompts import SYSTEM_PROMPT, TASK_PROMPT_TEMPLATE
from app.llm.gemini_client import gemini_client
from app.core.workflow_logger import WorkflowLogger


class PlannerAgent:

    def __init__(self):

        self.logger = WorkflowLogger()

    def create_plan(self, task: str):

        self.logger.log("PlannerAgent", "Creating plan")

        prompt = SYSTEM_PROMPT + TASK_PROMPT_TEMPLATE.format(task=task)

        output = gemini_client.generate(prompt)

        steps = [
            line.strip().split(".",1)[-1].strip()
            for line in output.split("\n")
            if line.strip()
        ]

        self.logger.log("PlannerAgent", f"Generated Plan: {steps}")

        return steps