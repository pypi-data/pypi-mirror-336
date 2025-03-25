from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsZipTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsZipTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsZipTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsZipTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_use_dash_4_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsUseDash4Metadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsZipTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsZipTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsZipTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsZipTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsZipTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsZipTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsZipTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsUnderlineMetadata]):
        use_dash_4 (Optional[str]):  Example: string.
        use_dash_4_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsUseDash4Metadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsZipTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsBoldMetadata"] = Field(
        alias="boldMetadata", default=None
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsZipTabsErrorDetails"] = Field(
        alias="errorDetails", default=None
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsFontMetadata"] = Field(
        alias="fontMetadata", default=None
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsHeightMetadata"] = (
        Field(alias="heightMetadata", default=None)
    )
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsItalicMetadata"] = (
        Field(alias="italicMetadata", default=None)
    )
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsZipTabsLocalePolicy"] = Field(
        alias="localePolicy", default=None
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsLockedMetadata"] = (
        Field(alias="lockedMetadata", default=None)
    )
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsZipTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsNameMetadata"] = Field(
        alias="nameMetadata", default=None
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsSharedMetadata"] = (
        Field(alias="sharedMetadata", default=None)
    )
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsStatusMetadata"] = (
        Field(alias="statusMetadata", default=None)
    )
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    use_dash_4: Optional[str] = Field(alias="useDash4", default=None)
    use_dash_4_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsUseDash4Metadata"
    ] = Field(alias="useDash4Metadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsZipTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsZipTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsZipTabsArrayItemRef"],
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
