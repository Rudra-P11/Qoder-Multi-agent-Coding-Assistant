import uuid

from app.database.crud import create_session


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
            "history": [],
            "language": None,
            "framework": None,
            "dependencies": []
        }

        create_session(session_id, prompt)

        return session_id

    def get_session(self, session_id):

        return self.sessions.get(session_id)

    def update_plan(self, session_id, plan):

        self.sessions[session_id]["plan"] = plan

    def approve_plan(self, session_id):

        self.sessions[session_id]["approved"] = True

    def set_language(self, session_id, language):

        self.sessions[session_id]["language"] = language

    def set_framework(self, session_id, framework):

        self.sessions[session_id]["framework"] = framework

    def set_dependencies(self, session_id, dependencies):

        self.sessions[session_id]["dependencies"] = dependencies


session_manager = SessionManager()