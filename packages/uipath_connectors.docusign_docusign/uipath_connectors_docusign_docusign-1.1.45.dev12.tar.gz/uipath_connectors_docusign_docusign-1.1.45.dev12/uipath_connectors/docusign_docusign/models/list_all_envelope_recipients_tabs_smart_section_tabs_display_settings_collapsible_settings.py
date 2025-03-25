from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettingsCollapsibleSettings(
    BaseModel
):
    """
    Attributes:
        arrow_closed (Optional[str]):  Example: string.
        arrow_color (Optional[str]):  Example: string.
        arrow_location (Optional[str]):  Example: string.
        arrow_open (Optional[str]):  Example: string.
        arrow_size (Optional[str]):  Example: string.
        arrow_style (Optional[str]):  Example: string.
        container_style (Optional[str]):  Example: string.
        label_style (Optional[str]):  Example: string.
        only_arrow_is_clickable (Optional[bool]):  Example: True.
        outer_label_and_arrow_style (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    arrow_closed: Optional[str] = Field(alias="arrowClosed", default=None)
    arrow_color: Optional[str] = Field(alias="arrowColor", default=None)
    arrow_location: Optional[str] = Field(alias="arrowLocation", default=None)
    arrow_open: Optional[str] = Field(alias="arrowOpen", default=None)
    arrow_size: Optional[str] = Field(alias="arrowSize", default=None)
    arrow_style: Optional[str] = Field(alias="arrowStyle", default=None)
    container_style: Optional[str] = Field(alias="containerStyle", default=None)
    label_style: Optional[str] = Field(alias="labelStyle", default=None)
    only_arrow_is_clickable: Optional[bool] = Field(
        alias="onlyArrowIsClickable", default=None
    )
    outer_label_and_arrow_style: Optional[str] = Field(
        alias="outerLabelAndArrowStyle", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettingsCollapsibleSettings"
        ],
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
