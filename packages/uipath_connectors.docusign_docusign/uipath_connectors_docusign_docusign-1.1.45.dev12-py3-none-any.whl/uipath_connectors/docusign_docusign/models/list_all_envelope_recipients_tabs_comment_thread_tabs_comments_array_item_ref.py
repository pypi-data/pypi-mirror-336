from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListAllEnvelopeRecipientsTabsCommentThreadTabsCommentsArrayItemRef(BaseModel):
    """
    Attributes:
        envelope_id (Optional[str]):  Example: string.
        hmac (Optional[str]):  Example: string.
        id (Optional[str]):  Example: string.
        mentions (Optional[list[str]]):
        read (Optional[bool]):  Example: True.
        sent_by_email (Optional[str]):  Example: string.
        sent_by_full_name (Optional[str]):  Example: string.
        sent_by_image_id (Optional[str]):  Example: string.
        sent_by_initials (Optional[str]):  Example: string.
        sent_by_recipient_id (Optional[str]):  Example: string.
        sent_by_user_id (Optional[str]):  Example: string.
        signing_group_id (Optional[str]):  Example: string.
        signing_group_name (Optional[str]):  Example: string.
        subject (Optional[str]):  Example: string.
        tab_id (Optional[str]):  Example: string.
        text (Optional[str]):  Example: string.
        thread_id (Optional[str]):  Example: string.
        thread_originator_id (Optional[str]):  Example: string.
        time_stamp_formatted (Optional[str]):  Example: string.
        timestamp (Optional[str]):  Example: string.
        visible_to (Optional[list[str]]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)
    hmac: Optional[str] = Field(alias="hmac", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    mentions: Optional[list[str]] = Field(alias="mentions", default=None)
    read: Optional[bool] = Field(alias="read", default=None)
    sent_by_email: Optional[str] = Field(alias="sentByEmail", default=None)
    sent_by_full_name: Optional[str] = Field(alias="sentByFullName", default=None)
    sent_by_image_id: Optional[str] = Field(alias="sentByImageId", default=None)
    sent_by_initials: Optional[str] = Field(alias="sentByInitials", default=None)
    sent_by_recipient_id: Optional[str] = Field(alias="sentByRecipientId", default=None)
    sent_by_user_id: Optional[str] = Field(alias="sentByUserId", default=None)
    signing_group_id: Optional[str] = Field(alias="signingGroupId", default=None)
    signing_group_name: Optional[str] = Field(alias="signingGroupName", default=None)
    subject: Optional[str] = Field(alias="subject", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    text: Optional[str] = Field(alias="text", default=None)
    thread_id: Optional[str] = Field(alias="threadId", default=None)
    thread_originator_id: Optional[str] = Field(
        alias="threadOriginatorId", default=None
    )
    time_stamp_formatted: Optional[str] = Field(
        alias="timeStampFormatted", default=None
    )
    timestamp: Optional[str] = Field(alias="timestamp", default=None)
    visible_to: Optional[list[str]] = Field(alias="visibleTo", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCommentThreadTabsCommentsArrayItemRef"],
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
