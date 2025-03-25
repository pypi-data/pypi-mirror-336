from enum import Enum


class CreateEnvelopeRequestStatus(str, Enum):
    CREATED = "created"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
