from enum import Enum


class CreateEnvelopeUsingTemplateResponseStatus(str, Enum):
    DRAFT = "Draft"
    SEND = "Send"

    def __str__(self) -> str:
        return str(self.value)
