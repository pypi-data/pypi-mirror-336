from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_display_settings_collapsible_settings import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettingsCollapsibleSettings,
)


class ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettings(BaseModel):
    """
    Attributes:
        cell_style (Optional[str]):  Example: string.
        collapsible_settings
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettingsCollapsibleSettings]):
        display (Optional[str]):  Example: string.
        display_label (Optional[str]):  Example: string.
        display_order (Optional[int]):
        display_page_number (Optional[int]):
        hide_label_when_opened (Optional[bool]):  Example: True.
        inline_outer_style (Optional[str]):  Example: string.
        label_when_opened (Optional[str]):  Example: string.
        pre_label (Optional[str]):  Example: string.
        scroll_to_top_when_opened (Optional[bool]):  Example: True.
        table_style (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    cell_style: Optional[str] = Field(alias="cellStyle", default=None)
    collapsible_settings: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettingsCollapsibleSettings"
    ] = Field(alias="collapsibleSettings", default=None)
    display: Optional[str] = Field(alias="display", default=None)
    display_label: Optional[str] = Field(alias="displayLabel", default=None)
    display_order: Optional[int] = Field(alias="displayOrder", default=None)
    display_page_number: Optional[int] = Field(alias="displayPageNumber", default=None)
    hide_label_when_opened: Optional[bool] = Field(
        alias="hideLabelWhenOpened", default=None
    )
    inline_outer_style: Optional[str] = Field(alias="inlineOuterStyle", default=None)
    label_when_opened: Optional[str] = Field(alias="labelWhenOpened", default=None)
    pre_label: Optional[str] = Field(alias="preLabel", default=None)
    scroll_to_top_when_opened: Optional[bool] = Field(
        alias="scrollToTopWhenOpened", default=None
    )
    table_style: Optional[str] = Field(alias="tableStyle", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettings"],
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
