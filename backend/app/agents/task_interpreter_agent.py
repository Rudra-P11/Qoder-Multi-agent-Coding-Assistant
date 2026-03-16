from app.llm.ollama_client import ollama_client
from app.llm.prompts import TASK_INTERPRETER_PROMPT


class TaskInterpreterAgent:

    def interpret(self, task):

        prompt = TASK_INTERPRETER_PROMPT.format(task=task)

        response = ollama_client.generate(prompt)


        return response