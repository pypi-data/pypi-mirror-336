from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEnvelopeResponseEnvelopeAttachmentsArrayItemRef(BaseModel):
    """
    Attributes:
        access_control (Optional[str]):
        attachment_id (Optional[str]):
        attachment_type (Optional[str]):
        data (Optional[str]):
        label (Optional[str]):
        name (Optional[str]):
        remote_url (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access_control: Optional[str] = Field(alias="accessControl", default=None)
    attachment_id: Optional[str] = Field(alias="attachmentId", default=None)
    attachment_type: Optional[str] = Field(alias="attachmentType", default=None)
    data: Optional[str] = Field(alias="data", default=None)
    label: Optional[str] = Field(alias="label", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    remote_url: Optional[str] = Field(alias="remoteUrl", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseEnvelopeAttachmentsArrayItemRef"],
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
