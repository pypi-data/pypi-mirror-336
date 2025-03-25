from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_group_name_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsGroupNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_array_item_ref import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_tooltip_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsTooltipMetadata,
)


class ListAllEnvelopeRecipientsTabsRadioGroupTabsArrayItemRef(BaseModel):
    """
    Attributes:
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsConditionalParentValueMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsDocumentIdMetadata]):
        group_name (Optional[str]):  Example: string.
        group_name_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsGroupNameMetadata]):
        radios (Optional[list['ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosArrayItemRef']]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRequireInitialOnSharedChangeMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsSharedMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsTemplateRequiredMetadata]):
        tooltip (Optional[str]):  Example: string.
        tooltip_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsTooltipMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    group_name: Optional[str] = Field(alias="groupName", default=None)
    group_name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsGroupNameMetadata"
    ] = Field(alias="groupNameMetadata", default=None)
    radios: Optional[
        list["ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosArrayItemRef"]
    ] = Field(alias="radios", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    tooltip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsTooltipMetadata"
    ] = Field(alias="tooltipMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsRadioGroupTabsArrayItemRef"],
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
