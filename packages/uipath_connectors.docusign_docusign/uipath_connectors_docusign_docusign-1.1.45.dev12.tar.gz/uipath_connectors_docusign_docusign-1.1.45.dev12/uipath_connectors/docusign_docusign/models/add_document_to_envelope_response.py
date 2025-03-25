from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.add_document_to_envelope_response_envelope_documents_array_item_ref import (
    AddDocumentToEnvelopeResponseEnvelopeDocumentsArrayItemRef,
)


class AddDocumentToEnvelopeResponse(BaseModel):
    """
    Attributes:
        envelope_documents (Optional[list['AddDocumentToEnvelopeResponseEnvelopeDocumentsArrayItemRef']]):
        envelope_id (Optional[str]): Type the name or ID of the envelope. If the envelope is not found in the drop-down,
                you can first scroll the drop-down till the bottom to get all the available envelopes and then type the envelope
                or retrieve the envelope ID from the DocuSign application -> "Manage" tab -> Goto “Sent” or “Draft” under
                “Envelopes” -> Click on the respective envelope and retrieve the envelope ID from URL. For example, if the URL
                is “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the envelope ID is
                “3ae67e54-f761-4a5b-a23e-b5e4835492cc" Example: 01bdd3c9-6174-43f1-aaa9-5210f5c098eb.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    envelope_documents: Optional[
        list["AddDocumentToEnvelopeResponseEnvelopeDocumentsArrayItemRef"]
    ] = Field(alias="envelopeDocuments", default=None)
    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["AddDocumentToEnvelopeResponse"], src_dict: Dict[str, Any]):
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
