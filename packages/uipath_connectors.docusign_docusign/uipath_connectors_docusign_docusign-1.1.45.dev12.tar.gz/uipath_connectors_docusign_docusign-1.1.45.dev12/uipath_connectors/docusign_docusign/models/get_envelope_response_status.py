from enum import Enum


class GetEnvelopeResponseStatus(str, Enum):
    COMPLETED = "completed"
    CREATED = "created"
    DECLINED = "declined"
    DELETED = "deleted"
    DELIVERED = "delivered"
    PROCESSING = "processing"
    SENT = "sent"
    SIGNED = "signed"
    TIMEDOUT = "timedout"
    VOIDED = "voided"

    def __str__(self) -> str:
        return str(self.value)
