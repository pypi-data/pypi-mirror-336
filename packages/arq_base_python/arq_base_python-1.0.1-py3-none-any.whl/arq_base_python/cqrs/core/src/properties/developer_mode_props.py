import uuid


class DeveloperModeProps:
    def __init__(self, developer_mode=False):
        self.developer_mode = developer_mode
        self.devid = None
        if self.developer_mode:
            self.devid = str(uuid.uuid4())

    def is_developer_mode(self) -> bool:
        return self.developer_mode

    def set_developer_mode(self, developer_mode: bool):
        self.developer_mode = developer_mode

    def get_devid(self) -> str:
        return self.devid

    def set_devid(self, devid: str):
        self.devid = devid
