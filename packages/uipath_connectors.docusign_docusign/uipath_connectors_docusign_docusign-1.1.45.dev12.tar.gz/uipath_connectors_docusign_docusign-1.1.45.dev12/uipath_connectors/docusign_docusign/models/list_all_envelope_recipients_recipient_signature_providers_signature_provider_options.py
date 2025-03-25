from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_recipient_signature_providers_signature_provider_options_cpf_number_metadata import (
    ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsCpfNumberMetadata,
)
from ..models.list_all_envelope_recipients_recipient_signature_providers_signature_provider_options_one_time_password_metadata import (
    ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsOneTimePasswordMetadata,
)
from ..models.list_all_envelope_recipients_recipient_signature_providers_signature_provider_options_signer_role_metadata import (
    ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsSignerRoleMetadata,
)
from ..models.list_all_envelope_recipients_recipient_signature_providers_signature_provider_options_sms_metadata import (
    ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsSmsMetadata,
)


class ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptions(
    BaseModel
):
    """
    Attributes:
        cpf_number (Optional[str]):  Example: string.
        cpf_number_metadata
                (Optional[ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsCpfNumberMetadata]):
        one_time_password (Optional[str]):  Example: string.
        one_time_password_metadata
                (Optional[ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsOneTimePasswordMetadata]):
        signer_role (Optional[str]):  Example: string.
        signer_role_metadata
                (Optional[ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsSignerRoleMetadata]):
        sms (Optional[str]):  Example: string.
        sms_metadata
                (Optional[ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsSmsMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cpf_number: Optional[str] = Field(alias="cpfNumber", default=None)
    cpf_number_metadata: Optional[
        "ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsCpfNumberMetadata"
    ] = Field(alias="cpfNumberMetadata", default=None)
    one_time_password: Optional[str] = Field(alias="oneTimePassword", default=None)
    one_time_password_metadata: Optional[
        "ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsOneTimePasswordMetadata"
    ] = Field(alias="oneTimePasswordMetadata", default=None)
    signer_role: Optional[str] = Field(alias="signerRole", default=None)
    signer_role_metadata: Optional[
        "ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsSignerRoleMetadata"
    ] = Field(alias="signerRoleMetadata", default=None)
    sms: Optional[str] = Field(alias="sms", default=None)
    sms_metadata: Optional[
        "ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptionsSmsMetadata"
    ] = Field(alias="smsMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListAllEnvelopeRecipientsRecipientSignatureProvidersSignatureProviderOptions"
        ],
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
