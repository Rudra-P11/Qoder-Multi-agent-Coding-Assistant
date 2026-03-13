import uuid


class SessionManager:

    def __init__(self):
        self.sessions = {}

    def create_session(self, prompt):

        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "prompt": prompt,
            "plan": [],
            "approved": False,
            "todo": [],
            "history": []
        }

        return session_id

    def get_session(self, session_id):

        return self.sessions.get(session_id)

    def update_plan(self, session_id, plan):

        self.sessions[session_id]["plan"] = plan

    def approve_plan(self, session_id):

        self.sessions[session_id]["approved"] = True

session_manager = SessionManager()