from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_envelope_response_notification_expirations import (
    GetEnvelopeResponseNotificationExpirations,
)
from ..models.get_envelope_response_notification_reminders import (
    GetEnvelopeResponseNotificationReminders,
)


class GetEnvelopeResponseNotification(BaseModel):
    """
    Attributes:
        expirations (Optional[GetEnvelopeResponseNotificationExpirations]):
        reminders (Optional[GetEnvelopeResponseNotificationReminders]):
        use_account_defaults (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    expirations: Optional["GetEnvelopeResponseNotificationExpirations"] = Field(
        alias="expirations", default=None
    )
    reminders: Optional["GetEnvelopeResponseNotificationReminders"] = Field(
        alias="reminders", default=None
    )
    use_account_defaults: Optional[str] = Field(
        alias="useAccountDefaults", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseNotification"], src_dict: Dict[str, Any]
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
