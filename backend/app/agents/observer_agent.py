class ObserverAgent:

    def analyze_result(self, result):

        if result["exit_code"] == 0:

            return {
                "status": "success",
                "message": "Execution successful"
            }

        else:

            return {
                "status": "error",
                "message": result["stderr"]
            }