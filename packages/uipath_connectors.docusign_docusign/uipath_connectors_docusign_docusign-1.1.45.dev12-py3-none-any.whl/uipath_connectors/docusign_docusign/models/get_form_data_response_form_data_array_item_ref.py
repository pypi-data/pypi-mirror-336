from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_form_data_response_form_data_error_details import (
    GetFormDataResponseFormDataErrorDetails,
)


class GetFormDataResponseFormDataArrayItemRef(BaseModel):
    """
    Attributes:
        error_details (Optional[GetFormDataResponseFormDataErrorDetails]):
        list_selected_value (Optional[str]):
        name (Optional[str]):
        numerical_value (Optional[str]):
        original_value (Optional[str]):
        value (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    error_details: Optional["GetFormDataResponseFormDataErrorDetails"] = Field(
        alias="errorDetails", default=None
    )
    list_selected_value: Optional[str] = Field(alias="listSelectedValue", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    numerical_value: Optional[str] = Field(alias="numericalValue", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    value: Optional[str] = Field(alias="value", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetFormDataResponseFormDataArrayItemRef"], src_dict: Dict[str, Any]
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
