from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsFullNameTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsFullNameTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsFullNameTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsFullNameTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsFullNameTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsFullNameTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsFullNameTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsFullNameTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsFullNameTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsFullNameTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsFullNameTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    merge_field: Optional["ListAllEnvelopeRecipientsTabsFullNameTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsFullNameTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFullNameTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsFullNameTabsArrayItemRef"],
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
