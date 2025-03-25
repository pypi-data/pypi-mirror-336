from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_button_text_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsButtonTextMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsApproveTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsApproveTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsApproveTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsApproveTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_approve_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsApproveTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsApproveTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsBoldMetadata]):
        button_text (Optional[str]):  Example: string.
        button_text_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsButtonTextMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsApproveTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsApproveTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsApproveTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsApproveTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsApproveTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsRecipientIdMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsApproveTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsUnderlineMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsApproveTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsApproveTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    button_text: Optional[str] = Field(alias="buttonText", default=None)
    button_text_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsButtonTextMetadata"
    ] = Field(alias="buttonTextMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsApproveTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsApproveTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsApproveTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    merge_field: Optional["ListAllEnvelopeRecipientsTabsApproveTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsApproveTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsApproveTabsArrayItemRef"],
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
