from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_group_name_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsGroupNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_tooltip_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTooltipMetadata,
)


class ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsArrayItemRef(BaseModel):
    """
    Attributes:
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsConditionalParentValueMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsDocumentIdMetadata]):
        group_name (Optional[str]):  Example: string.
        group_name_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsGroupNameMetadata]):
        radios (Optional[list['ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosArrayItemRef']]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRequireInitialOnSharedChangeMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsSharedMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTemplateRequiredMetadata]):
        tooltip (Optional[str]):  Example: string.
        tooltip_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTooltipMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    group_name: Optional[str] = Field(alias="groupName", default=None)
    group_name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsGroupNameMetadata"
    ] = Field(alias="groupNameMetadata", default=None)
    radios: Optional[
        list["ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosArrayItemRef"]
    ] = Field(alias="radios", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    tooltip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsTooltipMetadata"
    ] = Field(alias="tooltipMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsArrayItemRef"],
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
