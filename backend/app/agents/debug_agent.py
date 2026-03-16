from app.llm.ollama_client import ollama_client
from app.llm.prompts import DEBUG_AGENT_PROMPT


class DebugAgent:

    def fix_code(self, code, error):

        prompt = DEBUG_AGENT_PROMPT.format(error=error, code=code)

        fixed_code = ollama_client.generate(prompt)


        return fixed_code