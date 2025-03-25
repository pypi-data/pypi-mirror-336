from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_list_tabs_list_items_selected_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsListItemsSelectedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_list_items_text_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsListItemsTextMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_list_items_value_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsListItemsValueMetadata,
)


class ListAllEnvelopeRecipientsTabsListTabsListItemsArrayItemRef(BaseModel):
    """
    Attributes:
        selected (Optional[str]):  Example: string.
        selected_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsListItemsSelectedMetadata]):
        text (Optional[str]):  Example: string.
        text_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsListItemsTextMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsListItemsValueMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    selected: Optional[str] = Field(alias="selected", default=None)
    selected_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsListItemsSelectedMetadata"
    ] = Field(alias="selectedMetadata", default=None)
    text: Optional[str] = Field(alias="text", default=None)
    text_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsListItemsTextMetadata"
    ] = Field(alias="textMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsListItemsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsListTabsListItemsArrayItemRef"],
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
