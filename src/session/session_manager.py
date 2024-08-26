from src.utils.logger import Logger


class SessionManager:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.sessions = {}

    def create_session(self, session_id):
        self.logger.info(f"Creating new session: {session_id}")
        # Implement session creation logic here
        pass

    def close_session(self, session_id):
        self.logger.info(f"Closing session: {session_id}")
        # Implement session closing logic here
        pass
