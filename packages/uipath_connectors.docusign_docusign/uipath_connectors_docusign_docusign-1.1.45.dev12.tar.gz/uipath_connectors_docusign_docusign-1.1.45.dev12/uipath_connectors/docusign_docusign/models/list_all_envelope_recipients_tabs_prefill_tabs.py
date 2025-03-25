from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsArrayItemRef,
)


class ListAllEnvelopeRecipientsTabsPrefillTabs(BaseModel):
    """
    Attributes:
        checkbox_tabs (Optional[list['ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsArrayItemRef']]):
        radio_group_tabs (Optional[list['ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsArrayItemRef']]):
        sender_company_tabs (Optional[list['ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsArrayItemRef']]):
        sender_name_tabs (Optional[list['ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsArrayItemRef']]):
        tab_groups (Optional[list['ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsArrayItemRef']]):
        text_tabs (Optional[list['ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    checkbox_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsArrayItemRef"]
    ] = Field(alias="checkboxTabs", default=None)
    radio_group_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsArrayItemRef"]
    ] = Field(alias="radioGroupTabs", default=None)
    sender_company_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsArrayItemRef"]
    ] = Field(alias="senderCompanyTabs", default=None)
    sender_name_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsArrayItemRef"]
    ] = Field(alias="senderNameTabs", default=None)
    tab_groups: Optional[
        list["ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsArrayItemRef"]
    ] = Field(alias="tabGroups", default=None)
    text_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsArrayItemRef"]
    ] = Field(alias="textTabs", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPrefillTabs"], src_dict: Dict[str, Any]
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
