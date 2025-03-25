from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_document_visibility_error_details import (
    ListAllEnvelopeRecipientsDocumentVisibilityErrorDetails,
)


class ListAllEnvelopeRecipientsDocumentVisibilityArrayItemRef(BaseModel):
    """
    Attributes:
        document_id (Optional[str]):  Example: string.
        error_details (Optional[ListAllEnvelopeRecipientsDocumentVisibilityErrorDetails]):
        recipient_id (Optional[str]):  Example: string.
        rights (Optional[str]):  Example: string.
        visible (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    document_id: Optional[str] = Field(alias="documentId", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsDocumentVisibilityErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    rights: Optional[str] = Field(alias="rights", default=None)
    visible: Optional[str] = Field(alias="visible", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsDocumentVisibilityArrayItemRef"],
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
