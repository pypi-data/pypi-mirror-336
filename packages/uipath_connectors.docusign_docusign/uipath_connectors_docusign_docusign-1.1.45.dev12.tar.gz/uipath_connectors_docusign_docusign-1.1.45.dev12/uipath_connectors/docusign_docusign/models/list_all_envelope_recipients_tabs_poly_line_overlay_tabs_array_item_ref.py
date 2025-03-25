from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_graphics_context import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsGraphicsContext,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_overlay_type_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsOverlayTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_poly_lines_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsPolyLinesArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormPageNumberMetadata]):
        graphics_context (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsGraphicsContext]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsHeightMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsLockedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        overlay_type (Optional[str]):  Example: string.
        overlay_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsOverlayTypeMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsPageNumberMetadata]):
        poly_lines (Optional[list['ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsPolyLinesArrayItemRef']]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsRecipientIdMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    graphics_context: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsGraphicsContext"
    ] = Field(alias="graphicsContext", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    overlay_type: Optional[str] = Field(alias="overlayType", default=None)
    overlay_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsOverlayTypeMetadata"
    ] = Field(alias="overlayTypeMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    poly_lines: Optional[
        list["ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsPolyLinesArrayItemRef"]
    ] = Field(alias="polyLines", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsArrayItemRef"],
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
