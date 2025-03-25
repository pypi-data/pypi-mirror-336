from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsFormulaTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_formula_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsFormulaMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_hidden_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsHiddenMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_is_payment_amount_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsIsPaymentAmountMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsFormulaTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsFormulaTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_payment_details import (
    ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetails,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_round_decimal_places_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsRoundDecimalPlacesMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsFormulaTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsFormulaTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsFormPageNumberMetadata]):
        formula (Optional[str]):  Example: string.
        formula_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsFormulaMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsHeightMetadata]):
        hidden (Optional[str]):  Example: string.
        hidden_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsHiddenMetadata]):
        is_payment_amount_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsIsPaymentAmountMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsPageNumberMetadata]):
        payment_details (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetails]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsRequiredMetadata]):
        round_decimal_places (Optional[str]):  Example: string.
        round_decimal_places_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsRoundDecimalPlacesMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsUnderlineMetadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsFormulaTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsFormulaTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsFormulaTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    formula: Optional[str] = Field(alias="formula", default=None)
    formula_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsFormulaMetadata"
    ] = Field(alias="formulaMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    hidden: Optional[str] = Field(alias="hidden", default=None)
    hidden_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsHiddenMetadata"
    ] = Field(alias="hiddenMetadata", default=None)
    is_payment_amount_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsIsPaymentAmountMetadata"
    ] = Field(alias="isPaymentAmountMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsFormulaTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsFormulaTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsFormulaTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    payment_details: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetails"
    ] = Field(alias="paymentDetails", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    round_decimal_places: Optional[str] = Field(
        alias="roundDecimalPlaces", default=None
    )
    round_decimal_places_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsRoundDecimalPlacesMetadata"
    ] = Field(alias="roundDecimalPlacesMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsFormulaTabsArrayItemRef"],
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
