from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsFirstNameTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsFirstNameTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsFirstNameTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFirstNameTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsFirstNameTabsArrayItemRef"],
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
