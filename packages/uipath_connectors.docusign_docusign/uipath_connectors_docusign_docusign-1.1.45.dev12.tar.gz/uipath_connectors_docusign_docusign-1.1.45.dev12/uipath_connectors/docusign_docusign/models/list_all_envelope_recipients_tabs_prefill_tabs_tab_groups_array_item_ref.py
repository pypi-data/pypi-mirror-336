from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_error_details import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_group_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsGroupLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_group_rule_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsGroupRuleMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_height_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_maximum_allowed_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMaximumAllowedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_merge_field import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_minimum_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMinimumRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_status_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_tab_scope_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabScopeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_width_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_tab_groups_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormPageNumberMetadata]):
        group_label (Optional[str]):  Example: string.
        group_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsGroupLabelMetadata]):
        group_rule (Optional[str]):  Example: string.
        group_rule_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsGroupRuleMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsHeightMetadata]):
        maximum_allowed (Optional[str]):  Example: string.
        maximum_allowed_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMaximumAllowedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        minimum_required (Optional[str]):  Example: string.
        minimum_required_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMinimumRequiredMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsRecipientIdMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabIdMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabOrderMetadata]):
        tab_scope (Optional[str]):  Example: string.
        tab_scope_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabScopeMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsValidationMessageMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    group_label: Optional[str] = Field(alias="groupLabel", default=None)
    group_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsGroupLabelMetadata"
    ] = Field(alias="groupLabelMetadata", default=None)
    group_rule: Optional[str] = Field(alias="groupRule", default=None)
    group_rule_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsGroupRuleMetadata"
    ] = Field(alias="groupRuleMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    maximum_allowed: Optional[str] = Field(alias="maximumAllowed", default=None)
    maximum_allowed_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMaximumAllowedMetadata"
    ] = Field(alias="maximumAllowedMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    minimum_required: Optional[str] = Field(alias="minimumRequired", default=None)
    minimum_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsMinimumRequiredMetadata"
    ] = Field(alias="minimumRequiredMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_scope: Optional[str] = Field(alias="tabScope", default=None)
    tab_scope_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabScopeMetadata"
    ] = Field(alias="tabScopeMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPrefillTabsTabGroupsArrayItemRef"],
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
