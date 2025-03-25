from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsEmailTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsEmailTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsEmailTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsEmailTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsEmailTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsEmailTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsEmailTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsEmailTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsEmailTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsEmailTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsUnderlineMetadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsEmailTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsEmailTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsEmailTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsEmailTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsEmailTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsEmailTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsEmailTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsEmailTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsEmailTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsEmailTabsArrayItemRef"],
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
