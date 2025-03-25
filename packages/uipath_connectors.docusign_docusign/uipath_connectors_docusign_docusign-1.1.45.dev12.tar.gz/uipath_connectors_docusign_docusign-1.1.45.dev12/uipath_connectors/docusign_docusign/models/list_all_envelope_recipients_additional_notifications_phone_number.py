from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_additional_notifications_phone_number_country_code_metadata import (
    ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumberCountryCodeMetadata,
)
from ..models.list_all_envelope_recipients_additional_notifications_phone_number_number_metadata import (
    ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumberNumberMetadata,
)


class ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumber(BaseModel):
    """
    Attributes:
        country_code (Optional[str]):  Example: string.
        country_code_metadata
                (Optional[ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumberCountryCodeMetadata]):
        number (Optional[str]):  Example: string.
        number_metadata (Optional[ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumberNumberMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    country_code: Optional[str] = Field(alias="countryCode", default=None)
    country_code_metadata: Optional[
        "ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumberCountryCodeMetadata"
    ] = Field(alias="countryCodeMetadata", default=None)
    number: Optional[str] = Field(alias="number", default=None)
    number_metadata: Optional[
        "ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumberNumberMetadata"
    ] = Field(alias="numberMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumber"],
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
