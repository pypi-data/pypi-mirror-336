from enum import Enum


class CreateByCopyingEnvelopeResponseStatus(str, Enum):
    CREATED = "created"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
