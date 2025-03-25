from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_formula_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormulaMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_text_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormPageNumberMetadata]):
        formula (Optional[str]):  Example: string.
        formula_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormulaMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsUnderlineMetadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    formula: Optional[str] = Field(alias="formula", default=None)
    formula_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsFormulaMetadata"
    ] = Field(alias="formulaMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPrefillTabsTextTabsArrayItemRef"],
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
