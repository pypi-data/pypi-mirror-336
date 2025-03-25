from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_email_notification_email_body_metadata import (
    ListAllEnvelopeRecipientsEmailNotificationEmailBodyMetadata,
)
from ..models.list_all_envelope_recipients_email_notification_email_subject_metadata import (
    ListAllEnvelopeRecipientsEmailNotificationEmailSubjectMetadata,
)
from ..models.list_all_envelope_recipients_email_notification_supported_language_metadata import (
    ListAllEnvelopeRecipientsEmailNotificationSupportedLanguageMetadata,
)


class ListAllEnvelopeRecipientsEmailNotification(BaseModel):
    """
    Attributes:
        email_body (Optional[str]):  Example: string.
        email_body_metadata (Optional[ListAllEnvelopeRecipientsEmailNotificationEmailBodyMetadata]):
        email_subject (Optional[str]):  Example: string.
        email_subject_metadata (Optional[ListAllEnvelopeRecipientsEmailNotificationEmailSubjectMetadata]):
        supported_language (Optional[str]):  Example: string.
        supported_language_metadata (Optional[ListAllEnvelopeRecipientsEmailNotificationSupportedLanguageMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    email_body: Optional[str] = Field(alias="emailBody", default=None)
    email_body_metadata: Optional[
        "ListAllEnvelopeRecipientsEmailNotificationEmailBodyMetadata"
    ] = Field(alias="emailBodyMetadata", default=None)
    email_subject: Optional[str] = Field(alias="emailSubject", default=None)
    email_subject_metadata: Optional[
        "ListAllEnvelopeRecipientsEmailNotificationEmailSubjectMetadata"
    ] = Field(alias="emailSubjectMetadata", default=None)
    supported_language: Optional[str] = Field(alias="supportedLanguage", default=None)
    supported_language_metadata: Optional[
        "ListAllEnvelopeRecipientsEmailNotificationSupportedLanguageMetadata"
    ] = Field(alias="supportedLanguageMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsEmailNotification"],
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
