from enum import Enum


class CreateEnvelopeResponseStatus(str, Enum):
    CREATED = "created"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
