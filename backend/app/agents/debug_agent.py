from app.llm.ollama_client import ollama_client


class DebugAgent:

    def fix_code(self, code, error):

        prompt = f"""
The following code failed.

Error:
{error}

Code:
{code}

Fix the code and return the corrected Python script.
"""

        fixed_code = ollama_client.generate(prompt)

        return fixed_code