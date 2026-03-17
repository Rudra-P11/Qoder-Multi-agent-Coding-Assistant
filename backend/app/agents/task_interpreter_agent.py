from app.llm.gemini_client import gemini_client
from app.llm.prompts import TASK_INTERPRETER_PROMPT
import json


class TaskInterpreterAgent:

    def interpret(self, task):

        prompt = TASK_INTERPRETER_PROMPT.format(task=task)

        output = gemini_client.generate_json(prompt)


        return json.loads(output)