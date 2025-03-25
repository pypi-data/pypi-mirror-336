from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEnvelopeResponseNotificationExpirations(BaseModel):
    """
    Attributes:
        expire_after (Optional[str]):
        expire_enabled (Optional[str]):
        expire_warn (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    expire_after: Optional[str] = Field(alias="expireAfter", default=None)
    expire_enabled: Optional[str] = Field(alias="expireEnabled", default=None)
    expire_warn: Optional[str] = Field(alias="expireWarn", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseNotificationExpirations"],
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
