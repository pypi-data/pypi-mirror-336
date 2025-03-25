from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPhoneNumberTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsRequiredMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPhoneNumberTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsPhoneNumberTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPhoneNumberTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPhoneNumberTabsArrayItemRef"],
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
