from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_sender_company_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsRecipientIdMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListAllEnvelopeRecipientsTabsPrefillTabsSenderCompanyTabsArrayItemRef"
        ],
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
