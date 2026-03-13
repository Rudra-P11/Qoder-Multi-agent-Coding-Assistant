from app.tools.tool_registry import TOOL_REGISTRY


class ActionValidator:

    def validate(self, action):

        tool = action.get("action")

        if tool not in TOOL_REGISTRY:

            return False

        return True


action_validator = ActionValidator()