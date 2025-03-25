from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEnvelopeResponsePowerForm(BaseModel):
    """
    Attributes:
        created_by (Optional[str]):
        created_date_time (Optional[str]):
        email_body (Optional[str]):
        email_subject (Optional[str]):
        instructions (Optional[str]):
        is_active (Optional[str]):
        last_used (Optional[str]):
        limit_use_interval (Optional[str]):
        limit_use_interval_enabled (Optional[str]):
        limit_use_interval_units (Optional[str]):
        max_use_enabled (Optional[str]):
        name (Optional[str]):
        power_form_id (Optional[str]):
        power_form_url (Optional[str]):
        sender_name (Optional[str]):
        sender_user_id (Optional[str]):
        signing_mode (Optional[str]):
        template_id (Optional[str]):
        template_name (Optional[str]):
        times_used (Optional[str]):
        uri (Optional[str]):
        uses_remaining (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_by: Optional[str] = Field(alias="createdBy", default=None)
    created_date_time: Optional[str] = Field(alias="createdDateTime", default=None)
    email_body: Optional[str] = Field(alias="emailBody", default=None)
    email_subject: Optional[str] = Field(alias="emailSubject", default=None)
    instructions: Optional[str] = Field(alias="instructions", default=None)
    is_active: Optional[str] = Field(alias="isActive", default=None)
    last_used: Optional[str] = Field(alias="lastUsed", default=None)
    limit_use_interval: Optional[str] = Field(alias="limitUseInterval", default=None)
    limit_use_interval_enabled: Optional[str] = Field(
        alias="limitUseIntervalEnabled", default=None
    )
    limit_use_interval_units: Optional[str] = Field(
        alias="limitUseIntervalUnits", default=None
    )
    max_use_enabled: Optional[str] = Field(alias="maxUseEnabled", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    power_form_id: Optional[str] = Field(alias="powerFormId", default=None)
    power_form_url: Optional[str] = Field(alias="powerFormUrl", default=None)
    sender_name: Optional[str] = Field(alias="senderName", default=None)
    sender_user_id: Optional[str] = Field(alias="senderUserId", default=None)
    signing_mode: Optional[str] = Field(alias="signingMode", default=None)
    template_id: Optional[str] = Field(alias="templateId", default=None)
    template_name: Optional[str] = Field(alias="templateName", default=None)
    times_used: Optional[str] = Field(alias="timesUsed", default=None)
    uri: Optional[str] = Field(alias="uri", default=None)
    uses_remaining: Optional[str] = Field(alias="usesRemaining", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEnvelopeResponsePowerForm"], src_dict: Dict[str, Any]):
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
