from app.utils.logger import logger


class WorkflowLogger:

    def log(self, agent_name: str, message: str):

        logger.info(
            "agent_step",
            agent=agent_name,
            message=message
        )