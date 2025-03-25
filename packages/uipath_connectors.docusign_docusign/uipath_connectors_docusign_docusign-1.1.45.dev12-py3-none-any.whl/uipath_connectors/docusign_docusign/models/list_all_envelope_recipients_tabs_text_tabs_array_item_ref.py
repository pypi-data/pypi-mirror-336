from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsTextTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_formula_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsFormulaMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsTextTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsTextTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsTextTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsTextTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsTextTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsTextTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsFormPageNumberMetadata]):
        formula (Optional[str]):  Example: string.
        formula_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsFormulaMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsTextTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsTextTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTextTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsTextTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsUnderlineMetadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsTextTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsTextTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    formula: Optional[str] = Field(alias="formula", default=None)
    formula_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsFormulaMetadata"
    ] = Field(alias="formulaMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsHeightMetadata"] = (
        Field(alias="heightMetadata", default=None)
    )
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsItalicMetadata"] = (
        Field(alias="italicMetadata", default=None)
    )
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsTextTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsLockedMetadata"] = (
        Field(alias="lockedMetadata", default=None)
    )
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsTextTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsSharedMetadata"] = (
        Field(alias="sharedMetadata", default=None)
    )
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsStatusMetadata"] = (
        Field(alias="statusMetadata", default=None)
    )
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsTextTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTextTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsTextTabsArrayItemRef"],
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
