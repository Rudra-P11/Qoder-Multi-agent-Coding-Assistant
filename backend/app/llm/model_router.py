class ModelRouter:

    def select_model(self, task):

        length = len(task)

        if length < 200:

            return "gemini-2.5-flash"

        if length < 600:

            return "gemini-2.5-pro"

        return "gemini-2.5-pro"


model_router = ModelRouter()