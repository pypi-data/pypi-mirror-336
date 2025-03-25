from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsLastNameTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsLastNameTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsLastNameTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsLastNameTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsLastNameTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsLastNameTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsLastNameTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsLastNameTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsLastNameTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsLastNameTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsLastNameTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    merge_field: Optional["ListAllEnvelopeRecipientsTabsLastNameTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsLastNameTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsLastNameTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsLastNameTabsArrayItemRef"],
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
