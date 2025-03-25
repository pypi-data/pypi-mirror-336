from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_button_text_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsButtonTextMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_decline_reason_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsDeclineReasonMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsDeclineTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsDeclineTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsDeclineTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsDeclineTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsDeclineTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsDeclineTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsBoldMetadata]):
        button_text (Optional[str]):  Example: string.
        button_text_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsButtonTextMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsCustomTabIdMetadata]):
        decline_reason (Optional[str]):  Example: string.
        decline_reason_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsDeclineReasonMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsUnderlineMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDeclineTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsDeclineTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    button_text: Optional[str] = Field(alias="buttonText", default=None)
    button_text_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsButtonTextMetadata"
    ] = Field(alias="buttonTextMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    decline_reason: Optional[str] = Field(alias="declineReason", default=None)
    decline_reason_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsDeclineReasonMetadata"
    ] = Field(alias="declineReasonMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsDeclineTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsDeclineTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsDeclineTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    merge_field: Optional["ListAllEnvelopeRecipientsTabsDeclineTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDeclineTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsDeclineTabsArrayItemRef"],
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
