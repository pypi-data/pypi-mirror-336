from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class AddRecipientToEnvelopeResponseSignersArrayItemRef(BaseModel):
    """
    Attributes:
        completed_count (Optional[str]):  Example: 0.
        creation_reason (Optional[str]):  Example: sender.
        delivery_method (Optional[str]):  Example: email.
        email (Optional[str]):  Example: testing1@gmail.com.
        name (Optional[str]):  Example: test2.
        note (Optional[str]):  Example: please sign the document.
        recipient_id (Optional[str]):  Example: 4.
        recipient_type (Optional[str]):  Example: signer.
        require_id_lookup (Optional[str]):  Example: false.
        require_upload_signature (Optional[str]):  Example: false.
        routing_order (Optional[str]):  Example: 1.
        status (Optional[str]):  Example: created.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    completed_count: Optional[str] = Field(alias="completedCount", default=None)
    creation_reason: Optional[str] = Field(alias="creationReason", default=None)
    delivery_method: Optional[str] = Field(alias="deliveryMethod", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    note: Optional[str] = Field(alias="note", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_type: Optional[str] = Field(alias="recipientType", default=None)
    require_id_lookup: Optional[str] = Field(alias="requireIdLookup", default=None)
    require_upload_signature: Optional[str] = Field(
        alias="requireUploadSignature", default=None
    )
    routing_order: Optional[str] = Field(alias="routingOrder", default=None)
    status: Optional[str] = Field(alias="status", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AddRecipientToEnvelopeResponseSignersArrayItemRef"],
        src_dict: Dict[str, Any],
    ):
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
