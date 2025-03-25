from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEnvelopeResponseFoldersFilter(BaseModel):
    """
    Attributes:
        action_required (Optional[str]):
        expires (Optional[str]):
        folder_ids (Optional[str]):
        from_date_time (Optional[str]):
        is_template (Optional[str]):
        order (Optional[str]):
        order_by (Optional[str]):
        search_target (Optional[str]):
        search_text (Optional[str]):
        status (Optional[str]):
        to_date_time (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    action_required: Optional[str] = Field(alias="actionRequired", default=None)
    expires: Optional[str] = Field(alias="expires", default=None)
    folder_ids: Optional[str] = Field(alias="folderIds", default=None)
    from_date_time: Optional[str] = Field(alias="fromDateTime", default=None)
    is_template: Optional[str] = Field(alias="isTemplate", default=None)
    order: Optional[str] = Field(alias="order", default=None)
    order_by: Optional[str] = Field(alias="orderBy", default=None)
    search_target: Optional[str] = Field(alias="searchTarget", default=None)
    search_text: Optional[str] = Field(alias="searchText", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    to_date_time: Optional[str] = Field(alias="toDateTime", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseFoldersFilter"], src_dict: Dict[str, Any]
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
