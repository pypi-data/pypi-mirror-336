from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsEnvelopeIdTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsUnderlineMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsEnvelopeIdTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsEnvelopeIdTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsEnvelopeIdTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsEnvelopeIdTabsArrayItemRef"],
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
