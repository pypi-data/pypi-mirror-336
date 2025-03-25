from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_recipient_signature_providers_signature_provider_name_metadata import (
    ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderNameMetadata,
)
from ..models.list_all_envelope_recipients_recipient_signature_providers_signature_provider_options import (
    ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptions,
)


class ListAllEnvelopeRecipientsRecipientSignatureProvidersArrayItemRef(BaseModel):
    """
    Attributes:
        seal_documents_with_tabs_only (Optional[str]):  Example: string.
        seal_name (Optional[str]):  Example: string.
        signature_provider_name (Optional[str]):  Example: string.
        signature_provider_name_metadata
                (Optional[ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderNameMetadata]):
        signature_provider_options
                (Optional[ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptions]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    seal_documents_with_tabs_only: Optional[str] = Field(
        alias="sealDocumentsWithTabsOnly", default=None
    )
    seal_name: Optional[str] = Field(alias="sealName", default=None)
    signature_provider_name: Optional[str] = Field(
        alias="signatureProviderName", default=None
    )
    signature_provider_name_metadata: Optional[
        "ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderNameMetadata"
    ] = Field(alias="signatureProviderNameMetadata", default=None)
    signature_provider_options: Optional[
        "ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptions"
    ] = Field(alias="signatureProviderOptions", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsRecipientSignatureProvidersArrayItemRef"],
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
