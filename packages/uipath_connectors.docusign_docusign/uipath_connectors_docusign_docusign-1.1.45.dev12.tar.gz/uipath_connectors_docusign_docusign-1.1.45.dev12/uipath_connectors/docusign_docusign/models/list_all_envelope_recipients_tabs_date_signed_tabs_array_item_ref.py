from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsDateSignedTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDateSignedTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsDateSignedTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDateSignedTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsDateSignedTabsArrayItemRef"],
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
