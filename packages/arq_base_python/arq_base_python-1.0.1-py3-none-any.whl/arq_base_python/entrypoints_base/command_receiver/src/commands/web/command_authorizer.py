import logging


class CommandAuthorizer:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def authorize_recieve_command(self, command, request) -> bool:
        return True
