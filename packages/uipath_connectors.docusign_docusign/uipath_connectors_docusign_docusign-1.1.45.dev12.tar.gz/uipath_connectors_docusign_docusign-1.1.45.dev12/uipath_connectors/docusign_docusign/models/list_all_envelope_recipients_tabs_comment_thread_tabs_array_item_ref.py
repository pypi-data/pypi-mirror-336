from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_comments_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsCommentsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCommentThreadTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsBoldMetadata]):
        comments (Optional[list['ListAllEnvelopeRecipientsTabsCommentThreadTabsCommentsArrayItemRef']]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsTemplateRequiredMetadata]):
        thread_id (Optional[str]):  Example: string.
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsUnderlineMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommentThreadTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    comments: Optional[
        list["ListAllEnvelopeRecipientsTabsCommentThreadTabsCommentsArrayItemRef"]
    ] = Field(alias="comments", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    thread_id: Optional[str] = Field(alias="threadId", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommentThreadTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCommentThreadTabsArrayItemRef"],
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
