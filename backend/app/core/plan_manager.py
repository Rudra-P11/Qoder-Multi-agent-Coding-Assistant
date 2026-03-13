from app.core.session_manager import session_manager

class PlanManager:

    def store_plan(self, session_id, plan):

        session_manager.update_plan(session_id, plan)

    def get_plan(self, session_id):

        session = session_manager.get_session(session_id)

        return session["plan"]

    def modify_plan(self, session_id, new_plan):

        session_manager.update_plan(session_id, new_plan)

        return new_plan

plan_manager = PlanManager()