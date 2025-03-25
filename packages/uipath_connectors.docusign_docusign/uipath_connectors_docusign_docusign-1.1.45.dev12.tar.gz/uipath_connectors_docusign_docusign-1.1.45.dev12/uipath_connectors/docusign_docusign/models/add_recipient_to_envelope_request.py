from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.add_recipient_to_envelope_request_recipient_type import (
    AddRecipientToEnvelopeRequestRecipientType,
)


class AddRecipientToEnvelopeRequest(BaseModel):
    """
    Attributes:
        recipient_email (str): The email address of the recipient. The system sends notifications about the documents to
                sign to this email. Example: testing1@gmail.com.
        recipient_name (str): The full legal name of the recipient Example: test2.
        recipient_id (Optional[str]):  Example: 4.
        recipient_note (Optional[str]): A note sent to the recipient in the signing email. This note is unique to this
                recipient Example: please sign the document.
        recipient_routing_order (Optional[int]): Specifies the signing order of the recipient in the envelope. For
                example, if 1 is assigned as the signing order for the recipient, the envelope will be routed to other
                recipients only if this recipient has signed the envelope. Example: 1.0.
        recipient_type (Optional[AddRecipientToEnvelopeRequestRecipientType]): The type associated with the recipient.
                Valid values can be “Signer”, “Agent”, “Editor” etc. Default value is signer. Example: signer.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    recipient_email: str = Field(alias="recipientEmail")
    recipient_name: str = Field(alias="recipientName")
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_note: Optional[str] = Field(alias="recipientNote", default=None)
    recipient_routing_order: Optional[int] = Field(
        alias="recipientRoutingOrder", default=None
    )
    recipient_type: Optional["AddRecipientToEnvelopeRequestRecipientType"] = Field(
        alias="recipientType", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["AddRecipientToEnvelopeRequest"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
