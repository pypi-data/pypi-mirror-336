from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_error_details import (
    ListAllEnvelopeRecipientsTabsTabGroupsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_group_label_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsGroupLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_group_rule_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsGroupRuleMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_height_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_maximum_allowed_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsMaximumAllowedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_merge_field import (
    ListAllEnvelopeRecipientsTabsTabGroupsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_minimum_required_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsMinimumRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsTabGroupsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_status_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_tab_scope_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsTabScopeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_width_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsTabGroupsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsTabGroupsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTabGroupsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTabGroupsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsTabGroupsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsFormPageNumberMetadata]):
        group_label (Optional[str]):  Example: string.
        group_label_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsGroupLabelMetadata]):
        group_rule (Optional[str]):  Example: string.
        group_rule_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsGroupRuleMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsHeightMetadata]):
        maximum_allowed (Optional[str]):  Example: string.
        maximum_allowed_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsMaximumAllowedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsTabGroupsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        minimum_required (Optional[str]):  Example: string.
        minimum_required_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsMinimumRequiredMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsTabGroupsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsTabIdMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsTabOrderMetadata]):
        tab_scope (Optional[str]):  Example: string.
        tab_scope_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsTabScopeMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsValidationMessageMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsTabGroupsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsTabGroupsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    group_label: Optional[str] = Field(alias="groupLabel", default=None)
    group_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsGroupLabelMetadata"
    ] = Field(alias="groupLabelMetadata", default=None)
    group_rule: Optional[str] = Field(alias="groupRule", default=None)
    group_rule_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsGroupRuleMetadata"
    ] = Field(alias="groupRuleMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    maximum_allowed: Optional[str] = Field(alias="maximumAllowed", default=None)
    maximum_allowed_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsMaximumAllowedMetadata"
    ] = Field(alias="maximumAllowedMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsTabGroupsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    minimum_required: Optional[str] = Field(alias="minimumRequired", default=None)
    minimum_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsMinimumRequiredMetadata"
    ] = Field(alias="minimumRequiredMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsTabGroupsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_scope: Optional[str] = Field(alias="tabScope", default=None)
    tab_scope_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsTabScopeMetadata"
    ] = Field(alias="tabScopeMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsTabGroupsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTabGroupsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsTabGroupsArrayItemRef"],
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
