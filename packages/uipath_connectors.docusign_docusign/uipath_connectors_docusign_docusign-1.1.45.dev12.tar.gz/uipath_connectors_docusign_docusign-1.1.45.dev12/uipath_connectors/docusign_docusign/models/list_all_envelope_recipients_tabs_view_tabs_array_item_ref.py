from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_button_text_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsButtonTextMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsViewTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsViewTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsViewTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsViewTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsViewTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsViewTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsBoldMetadata]):
        button_text (Optional[str]):  Example: string.
        button_text_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsButtonTextMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsViewTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsViewTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsViewTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsViewTabsLocalePolicy]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsViewTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsRequiredMetadata]):
        required_read (Optional[str]):  Example: string.
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsViewTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsUnderlineMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsViewTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsViewTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    button_text: Optional[str] = Field(alias="buttonText", default=None)
    button_text_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsButtonTextMetadata"
    ] = Field(alias="buttonTextMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsViewTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsViewTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional["ListAllEnvelopeRecipientsTabsViewTabsHeightMetadata"] = (
        Field(alias="heightMetadata", default=None)
    )
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional["ListAllEnvelopeRecipientsTabsViewTabsItalicMetadata"] = (
        Field(alias="italicMetadata", default=None)
    )
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsViewTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    merge_field: Optional["ListAllEnvelopeRecipientsTabsViewTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    required_read: Optional[str] = Field(alias="requiredRead", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional["ListAllEnvelopeRecipientsTabsViewTabsStatusMetadata"] = (
        Field(alias="statusMetadata", default=None)
    )
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsViewTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsViewTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsViewTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsViewTabsArrayItemRef"],
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
