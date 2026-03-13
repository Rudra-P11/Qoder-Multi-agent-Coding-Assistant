from app.memory.conversation_store import conversation_store
from app.memory.summarizer import summarizer


class MemoryManager:

    MAX_MESSAGES = 20

    def store_user_prompt(self, session_id, prompt):

        conversation_store.add_message(session_id, "user", prompt)

        self._compress_if_needed(session_id)

    def store_agent_message(self, session_id, message):

        conversation_store.add_message(session_id, "agent", message)

        self._compress_if_needed(session_id)

    def get_conversation(self, session_id):

        return conversation_store.get_history(session_id)

    def _compress_if_needed(self, session_id):

        history = conversation_store.get_history(session_id)

        if len(history) > self.MAX_MESSAGES:

            summary = summarizer.summarize(history)

            conversation_store.sessions[session_id] = [
                {"role": "summary", "content": summary}
            ]


memory_manager = MemoryManager()