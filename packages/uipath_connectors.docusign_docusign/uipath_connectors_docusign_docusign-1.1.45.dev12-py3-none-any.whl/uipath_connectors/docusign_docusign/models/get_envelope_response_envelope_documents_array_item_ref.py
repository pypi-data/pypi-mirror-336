from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_envelope_response_envelope_documents_authoritative_copy_metadata import (
    GetEnvelopeResponseEnvelopeDocumentsAuthoritativeCopyMetadata,
)
from ..models.get_envelope_response_envelope_documents_signer_must_acknowledge_metadata import (
    GetEnvelopeResponseEnvelopeDocumentsSignerMustAcknowledgeMetadata,
)


class GetEnvelopeResponseEnvelopeDocumentsArrayItemRef(BaseModel):
    """
    Attributes:
        added_recipient_ids (Optional[list[str]]):
        attachment_tab_id (Optional[str]):
        authoritative_copy (Optional[str]):
        authoritative_copy_metadata (Optional[GetEnvelopeResponseEnvelopeDocumentsAuthoritativeCopyMetadata]):
        contains_pdf_form_fields (Optional[str]):
        display (Optional[str]):
        document_base_64 (Optional[str]):
        document_id (Optional[str]):
        document_id_guid (Optional[str]):
        include_in_download (Optional[str]):
        name (Optional[str]):
        order (Optional[str]):
        signer_must_acknowledge (Optional[str]):
        signer_must_acknowledge_metadata (Optional[GetEnvelopeResponseEnvelopeDocumentsSignerMustAcknowledgeMetadata]):
        size_bytes (Optional[str]):
        template_locked (Optional[str]):
        template_required (Optional[str]):
        type_ (Optional[str]):
        uri (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    added_recipient_ids: Optional[list[str]] = Field(
        alias="addedRecipientIds", default=None
    )
    attachment_tab_id: Optional[str] = Field(alias="attachmentTabId", default=None)
    authoritative_copy: Optional[str] = Field(alias="authoritativeCopy", default=None)
    authoritative_copy_metadata: Optional[
        "GetEnvelopeResponseEnvelopeDocumentsAuthoritativeCopyMetadata"
    ] = Field(alias="authoritativeCopyMetadata", default=None)
    contains_pdf_form_fields: Optional[str] = Field(
        alias="containsPdfFormFields", default=None
    )
    display: Optional[str] = Field(alias="display", default=None)
    document_base_64: Optional[str] = Field(alias="documentBase64", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_guid: Optional[str] = Field(alias="documentIdGuid", default=None)
    include_in_download: Optional[str] = Field(alias="includeInDownload", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    order: Optional[str] = Field(alias="order", default=None)
    signer_must_acknowledge: Optional[str] = Field(
        alias="signerMustAcknowledge", default=None
    )
    signer_must_acknowledge_metadata: Optional[
        "GetEnvelopeResponseEnvelopeDocumentsSignerMustAcknowledgeMetadata"
    ] = Field(alias="signerMustAcknowledgeMetadata", default=None)
    size_bytes: Optional[str] = Field(alias="sizeBytes", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    type_: Optional[str] = Field(alias="type", default=None)
    uri: Optional[str] = Field(alias="uri", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseEnvelopeDocumentsArrayItemRef"],
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
