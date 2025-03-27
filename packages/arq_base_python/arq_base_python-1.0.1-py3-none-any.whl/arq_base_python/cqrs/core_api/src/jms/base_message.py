from typing import TypeVar, Dict
from typing import Generic

T = TypeVar("T")


class BaseMessage(Generic[T]):
    def __init__(self, body: T, headers: Dict[str, str], messageId: str = None, error: str = None):
        self.body = body
        self.headers = headers
        self.messageId = messageId
        self.error = error

    def get_body(self) -> T:
        return self.body

    def get_headers(self) -> Dict[str, str]:
        return self.headers

    def get_error(self) -> str:
        return self.error

    def get_message_id(self) -> str:
        return self.messageId

    def set_message_id(self, messageId: str):
        self.messageId = messageId

    def __repr__(self) -> str:
        return f"BaseMessage(body={self.body}, headers={self.headers}, messageId={self.messageId}), error={self.error}"
