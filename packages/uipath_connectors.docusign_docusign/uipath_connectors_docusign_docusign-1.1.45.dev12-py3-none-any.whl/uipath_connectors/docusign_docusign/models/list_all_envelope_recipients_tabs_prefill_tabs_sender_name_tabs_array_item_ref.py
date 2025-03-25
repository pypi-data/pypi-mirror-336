from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_name_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsRecipientIdMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsPrefillTabsSenderNameTabsArrayItemRef"],
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
