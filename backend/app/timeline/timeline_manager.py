class TimelineManager:

    def __init__(self):

        self.events = []

    def add_event(self, agent, message, data=None):

        event = {
            "agent": agent,
            "message": message,
            "data": data
        }

        self.events.append(event)

        return event

timeline_manager = TimelineManager()