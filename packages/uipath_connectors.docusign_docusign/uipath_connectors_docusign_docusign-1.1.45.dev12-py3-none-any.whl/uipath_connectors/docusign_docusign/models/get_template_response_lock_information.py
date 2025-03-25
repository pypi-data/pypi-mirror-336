from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_template_response_lock_information_error_details import (
    GetTemplateResponseLockInformationErrorDetails,
)
from ..models.get_template_response_lock_information_locked_by_user import (
    GetTemplateResponseLockInformationLockedByUser,
)


class GetTemplateResponseLockInformation(BaseModel):
    """
    Attributes:
        error_details (Optional[GetTemplateResponseLockInformationErrorDetails]):
        lock_duration_in_seconds (Optional[str]):
        lock_token (Optional[str]):
        lock_type (Optional[str]):
        locked_by_app (Optional[str]):
        locked_by_user (Optional[GetTemplateResponseLockInformationLockedByUser]):
        locked_until_date_time (Optional[str]):
        use_scratch_pad (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    error_details: Optional["GetTemplateResponseLockInformationErrorDetails"] = Field(
        alias="errorDetails", default=None
    )
    lock_duration_in_seconds: Optional[str] = Field(
        alias="lockDurationInSeconds", default=None
    )
    lock_token: Optional[str] = Field(alias="lockToken", default=None)
    lock_type: Optional[str] = Field(alias="lockType", default=None)
    locked_by_app: Optional[str] = Field(alias="lockedByApp", default=None)
    locked_by_user: Optional["GetTemplateResponseLockInformationLockedByUser"] = Field(
        alias="lockedByUser", default=None
    )
    locked_until_date_time: Optional[str] = Field(
        alias="lockedUntilDateTime", default=None
    )
    use_scratch_pad: Optional[str] = Field(alias="useScratchPad", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetTemplateResponseLockInformation"], src_dict: Dict[str, Any]
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
