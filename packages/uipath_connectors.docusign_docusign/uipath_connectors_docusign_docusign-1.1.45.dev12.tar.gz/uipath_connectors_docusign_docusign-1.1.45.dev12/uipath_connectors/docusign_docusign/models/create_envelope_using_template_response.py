from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_envelope_using_template_response_status import (
    CreateEnvelopeUsingTemplateResponseStatus,
)
import datetime


class CreateEnvelopeUsingTemplateResponse(BaseModel):
    """
    Attributes:
        status (CreateEnvelopeUsingTemplateResponseStatus): Indicates the envelope status. Valid values when creating an
                envelope are “draft” for creating a draft envelope or “send” for creating and sending the envelope to
                recipients. Example: Send.
        envelope_id (Optional[str]): Envelope ID which is created using template Example:
                8d68db59-96c1-4573-a6af-8ec3776b4356.
        status_date_time (Optional[datetime.datetime]):  Example: 2022-12-01T13:07:33.4387285Z.
        uri (Optional[str]):  Example: /envelopes/8d68db59-96c1-4573-a6af-8ec3776b4356.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    status: "CreateEnvelopeUsingTemplateResponseStatus" = Field(alias="status")
    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)
    status_date_time: Optional[datetime.datetime] = Field(
        alias="statusDateTime", default=None
    )
    uri: Optional[str] = Field(alias="uri", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateEnvelopeUsingTemplateResponse"], src_dict: Dict[str, Any]
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
