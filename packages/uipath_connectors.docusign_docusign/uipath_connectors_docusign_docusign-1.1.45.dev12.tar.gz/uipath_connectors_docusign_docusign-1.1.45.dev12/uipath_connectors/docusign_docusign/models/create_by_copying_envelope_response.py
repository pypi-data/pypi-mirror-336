from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_by_copying_envelope_response_status import (
    CreateByCopyingEnvelopeResponseStatus,
)
import datetime


class CreateByCopyingEnvelopeResponse(BaseModel):
    """
    Attributes:
        envelope_id (Optional[str]): Envelope ID which is created by copying an existing envelope Example:
                f8b82047-b054-4797-876e-9eb4308dee7d.
        status (Optional[CreateByCopyingEnvelopeResponseStatus]): Indicates the envelope status. Valid values when
                creating an envelope are “created” for creating a draft envelope or “sent” for creating and sending the envelope
                to recipients. Example: sent.
        status_date_time (Optional[datetime.datetime]):  Example: 2022-12-01T13:01:06.7982296Z.
        uri (Optional[str]):  Example: /envelopes/f8b82047-b054-4797-876e-9eb4308dee7d.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)
    status: Optional["CreateByCopyingEnvelopeResponseStatus"] = Field(
        alias="status", default=None
    )
    status_date_time: Optional[datetime.datetime] = Field(
        alias="statusDateTime", default=None
    )
    uri: Optional[str] = Field(alias="uri", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateByCopyingEnvelopeResponse"], src_dict: Dict[str, Any]
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
