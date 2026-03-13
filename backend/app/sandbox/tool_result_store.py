class ToolResultStore:

    def __init__(self):

        self.results = []

    def store(self, tool, result):

        self.results.append({
            "tool": tool,
            "result": result
        })

    def get_all(self):

        return self.results


tool_result_store = ToolResultStore()