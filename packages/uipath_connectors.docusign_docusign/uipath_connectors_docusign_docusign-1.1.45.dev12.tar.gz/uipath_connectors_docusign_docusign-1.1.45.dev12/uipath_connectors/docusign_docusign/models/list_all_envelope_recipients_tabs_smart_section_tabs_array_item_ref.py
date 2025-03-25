from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_display_settings import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettings,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_end_position import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsEndPosition,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_overlay_type_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsOverlayTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_start_position import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsStartPosition,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsSmartSectionTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorYOffsetMetadata]):
        case_sensitive (Optional[bool]):  Example: True.
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsCustomTabIdMetadata]):
        display_settings (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettings]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsDocumentIdMetadata]):
        end_anchor (Optional[str]):  Example: string.
        end_position (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsEndPosition]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsHeightMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsLockedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        overlay_type (Optional[str]):  Example: string.
        overlay_type_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsOverlayTypeMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsRecipientIdMetadata]):
        remove_end_anchor (Optional[bool]):  Example: True.
        remove_start_anchor (Optional[bool]):  Example: True.
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        start_anchor (Optional[str]):  Example: string.
        start_position (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsStartPosition]):
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSmartSectionTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    case_sensitive: Optional[bool] = Field(alias="caseSensitive", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    display_settings: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsDisplaySettings"
    ] = Field(alias="displaySettings", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    end_anchor: Optional[str] = Field(alias="endAnchor", default=None)
    end_position: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsEndPosition"
    ] = Field(alias="endPosition", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsSmartSectionTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    overlay_type: Optional[str] = Field(alias="overlayType", default=None)
    overlay_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsOverlayTypeMetadata"
    ] = Field(alias="overlayTypeMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    remove_end_anchor: Optional[bool] = Field(alias="removeEndAnchor", default=None)
    remove_start_anchor: Optional[bool] = Field(alias="removeStartAnchor", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    start_anchor: Optional[str] = Field(alias="startAnchor", default=None)
    start_position: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsStartPosition"
    ] = Field(alias="startPosition", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSmartSectionTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsSmartSectionTabsArrayItemRef"],
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
