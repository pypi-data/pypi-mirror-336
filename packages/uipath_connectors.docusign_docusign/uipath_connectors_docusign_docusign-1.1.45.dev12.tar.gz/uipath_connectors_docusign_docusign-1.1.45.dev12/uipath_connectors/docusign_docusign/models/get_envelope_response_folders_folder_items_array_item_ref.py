from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEnvelopeResponseFoldersFolderItemsArrayItemRef(BaseModel):
    """
    Attributes:
        completed_date_time (Optional[str]):
        created_date_time (Optional[str]):
        envelope_id (Optional[str]):
        envelope_uri (Optional[str]):
        expire_date_time (Optional[str]):
        folder_id (Optional[str]):
        folder_uri (Optional[str]):
        is_21cfr_part_11 (Optional[str]):
        owner_name (Optional[str]):
        recipients_uri (Optional[str]):
        sender_company (Optional[str]):
        sender_email (Optional[str]):
        sender_name (Optional[str]):
        sender_user_id (Optional[str]):
        sent_date_time (Optional[str]):
        status (Optional[str]):
        subject (Optional[str]):
        template_id (Optional[str]):
        template_uri (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    completed_date_time: Optional[str] = Field(alias="completedDateTime", default=None)
    created_date_time: Optional[str] = Field(alias="createdDateTime", default=None)
    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)
    envelope_uri: Optional[str] = Field(alias="envelopeUri", default=None)
    expire_date_time: Optional[str] = Field(alias="expireDateTime", default=None)
    folder_id: Optional[str] = Field(alias="folderId", default=None)
    folder_uri: Optional[str] = Field(alias="folderUri", default=None)
    is_21cfr_part_11: Optional[str] = Field(alias="is21CFRPart11", default=None)
    owner_name: Optional[str] = Field(alias="ownerName", default=None)
    recipients_uri: Optional[str] = Field(alias="recipientsUri", default=None)
    sender_company: Optional[str] = Field(alias="senderCompany", default=None)
    sender_email: Optional[str] = Field(alias="senderEmail", default=None)
    sender_name: Optional[str] = Field(alias="senderName", default=None)
    sender_user_id: Optional[str] = Field(alias="senderUserId", default=None)
    sent_date_time: Optional[str] = Field(alias="sentDateTime", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    subject: Optional[str] = Field(alias="subject", default=None)
    template_id: Optional[str] = Field(alias="templateId", default=None)
    template_uri: Optional[str] = Field(alias="templateUri", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseFoldersFolderItemsArrayItemRef"],
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
