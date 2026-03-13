from app.llm.gemini_client import gemini_client


class ConversationSummarizer:

    def summarize(self, conversation):

        prompt = f"""
Summarize the following conversation for future context.
Keep essential details and decisions, but be concise.
Write in a way that helps future agents understand the key points.

Conversation:
{conversation}

Return a short summary.
"""

        return gemini_client.generate(prompt)


summarizer = ConversationSummarizer()