from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_selected_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSelectedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_checkbox_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsItalicMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsLockedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRecipientIdMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRequiredMetadata]):
        selected (Optional[str]):  Example: string.
        selected_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSelectedMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSharedMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsUnderlineMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    selected: Optional[str] = Field(alias="selected", default=None)
    selected_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSelectedMetadata"
    ] = Field(alias="selectedMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPrefillTabsCheckboxTabsArrayItemRef"],
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
