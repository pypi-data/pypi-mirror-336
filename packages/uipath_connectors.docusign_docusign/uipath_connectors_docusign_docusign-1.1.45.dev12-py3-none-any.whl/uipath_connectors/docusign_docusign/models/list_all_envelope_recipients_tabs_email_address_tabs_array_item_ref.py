from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsEmailAddressTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsEmailAddressTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsEmailAddressTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEmailAddressTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsEmailAddressTabsArrayItemRef"],
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
