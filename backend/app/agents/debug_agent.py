from app.llm.gemini_client import gemini_client


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

        fixed_code = gemini_client.generate(prompt)

        return fixed_code