from enum import Enum


class AddRecipientToEnvelopeRequestRecipientType(str, Enum):
    AGENT = "agent"
    CARBON_COPY = "carbonCopy"
    CERTIFIED_DELIVERY = "certifiedDelivery"
    EDITOR = "editor"
    INTERMEDIARIES = "intermediaries"
    IN_PERSON_SIGNER = "inPersonSigner"
    SEAL = "seal"
    SIGNER = "signer"
    WITNESS = "witness"

    def __str__(self) -> str:
        return str(self.value)
