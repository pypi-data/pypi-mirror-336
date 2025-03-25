from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_envelope_response_status import CreateEnvelopeResponseStatus
import datetime


class CreateEnvelopeResponse(BaseModel):
    """
    Attributes:
        status (CreateEnvelopeResponseStatus): The status of the envelope. Example: sent.
        envelope_id (Optional[str]): A unique identifier for the envelope containing the document. Example:
                e2752d95-0fa7-4504-bb58-f0fc6e592f62.
        status_date_time (Optional[datetime.datetime]): The date and time when the envelope status was last updated.
                Example: 2024-12-12T04:59:23.3870000Z.
        uri (Optional[str]): The URI for accessing the envelope resource. Example:
                /envelopes/e2752d95-0fa7-4504-bb58-f0fc6e592f62.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    status: "CreateEnvelopeResponseStatus" = Field(alias="status")
    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)
    status_date_time: Optional[datetime.datetime] = Field(
        alias="statusDateTime", default=None
    )
    uri: Optional[str] = Field(alias="uri", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateEnvelopeResponse"], src_dict: Dict[str, Any]):
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
