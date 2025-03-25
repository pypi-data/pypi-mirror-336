from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsDateTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsDateTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsDateTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsDateTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsDateTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsDateTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsDateTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsDateTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsDateTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsDateTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsUnderlineMetadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDateTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsDateTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsHeightMetadata"] = (
        Field(alias="heightMetadata", default=None)
    )
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsItalicMetadata"] = (
        Field(alias="italicMetadata", default=None)
    )
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsDateTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsLockedMetadata"] = (
        Field(alias="lockedMetadata", default=None)
    )
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsDateTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsSharedMetadata"] = (
        Field(alias="sharedMetadata", default=None)
    )
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsStatusMetadata"] = (
        Field(alias="statusMetadata", default=None)
    )
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsDateTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsDateTabsArrayItemRef"],
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
