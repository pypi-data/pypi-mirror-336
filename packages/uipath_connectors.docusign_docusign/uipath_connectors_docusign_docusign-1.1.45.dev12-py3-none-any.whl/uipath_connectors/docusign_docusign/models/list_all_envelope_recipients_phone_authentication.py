from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_phone_authentication_recip_may_provide_number_metadata import (
    ListAllEnvelopeRecipientsPhoneAuthenticationRecipMayProvideNumberMetadata,
)
from ..models.list_all_envelope_recipients_phone_authentication_record_voice_print_metadata import (
    ListAllEnvelopeRecipientsPhoneAuthenticationRecordVoicePrintMetadata,
)
from ..models.list_all_envelope_recipients_phone_authentication_sender_provided_numbers_metadata import (
    ListAllEnvelopeRecipientsPhoneAuthenticationSenderProvidedNumbersMetadata,
)
from ..models.list_all_envelope_recipients_phone_authentication_validate_recip_provided_number_metadata import (
    ListAllEnvelopeRecipientsPhoneAuthenticationValidateRecipProvidedNumberMetadata,
)


class ListAllEnvelopeRecipientsPhoneAuthentication(BaseModel):
    """
    Attributes:
        recip_may_provide_number (Optional[str]):  Example: string.
        recip_may_provide_number_metadata
                (Optional[ListAllEnvelopeRecipientsPhoneAuthenticationRecipMayProvideNumberMetadata]):
        record_voice_print (Optional[str]):  Example: string.
        record_voice_print_metadata (Optional[ListAllEnvelopeRecipientsPhoneAuthenticationRecordVoicePrintMetadata]):
        sender_provided_numbers (Optional[list[str]]):
        sender_provided_numbers_metadata
                (Optional[ListAllEnvelopeRecipientsPhoneAuthenticationSenderProvidedNumbersMetadata]):
        validate_recip_provided_number (Optional[str]):  Example: string.
        validate_recip_provided_number_metadata
                (Optional[ListAllEnvelopeRecipientsPhoneAuthenticationValidateRecipProvidedNumberMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    recip_may_provide_number: Optional[str] = Field(
        alias="recipMayProvideNumber", default=None
    )
    recip_may_provide_number_metadata: Optional[
        "ListAllEnvelopeRecipientsPhoneAuthenticationRecipMayProvideNumberMetadata"
    ] = Field(alias="recipMayProvideNumberMetadata", default=None)
    record_voice_print: Optional[str] = Field(alias="recordVoicePrint", default=None)
    record_voice_print_metadata: Optional[
        "ListAllEnvelopeRecipientsPhoneAuthenticationRecordVoicePrintMetadata"
    ] = Field(alias="recordVoicePrintMetadata", default=None)
    sender_provided_numbers: Optional[list[str]] = Field(
        alias="senderProvidedNumbers", default=None
    )
    sender_provided_numbers_metadata: Optional[
        "ListAllEnvelopeRecipientsPhoneAuthenticationSenderProvidedNumbersMetadata"
    ] = Field(alias="senderProvidedNumbersMetadata", default=None)
    validate_recip_provided_number: Optional[str] = Field(
        alias="validateRecipProvidedNumber", default=None
    )
    validate_recip_provided_number_metadata: Optional[
        "ListAllEnvelopeRecipientsPhoneAuthenticationValidateRecipProvidedNumberMetadata"
    ] = Field(alias="validateRecipProvidedNumberMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsPhoneAuthentication"],
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
