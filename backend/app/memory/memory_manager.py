from app.memory.conversation_store import conversation_store


class MemoryManager:

    def store_user_prompt(self, session_id, prompt):

        conversation_store.add_message(
            session_id,
            "user",
            prompt
        )

    def store_agent_message(self, session_id, message):

        conversation_store.add_message(
            session_id,
            "agent",
            message
        )

    def get_conversation(self, session_id):

        return conversation_store.get_history(session_id)


memory_manager = MemoryManager()