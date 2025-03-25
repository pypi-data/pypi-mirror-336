from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsNumberTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_formula_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsFormulaMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsNumberTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsNumberTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsNumberTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsNumberTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsNumberTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsNumberTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsFormPageNumberMetadata]):
        formula (Optional[str]):  Example: string.
        formula_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsFormulaMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsNumberTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsNumberTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNumberTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsNumberTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsUnderlineMetadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsNumberTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsNumberTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsNumberTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsNumberTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    formula: Optional[str] = Field(alias="formula", default=None)
    formula_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsFormulaMetadata"
    ] = Field(alias="formulaMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsNumberTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsNumberTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsNumberTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsNumberTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsNumberTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNumberTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsNumberTabsArrayItemRef"],
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
