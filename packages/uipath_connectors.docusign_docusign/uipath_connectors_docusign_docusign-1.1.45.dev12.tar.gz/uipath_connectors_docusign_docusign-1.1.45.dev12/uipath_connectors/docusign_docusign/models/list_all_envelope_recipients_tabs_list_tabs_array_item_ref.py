from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsListTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_list_items_array_item_ref import (
    ListAllEnvelopeRecipientsTabsListTabsListItemsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_list_selected_value_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsListSelectedValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsListTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsListTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsListTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsListTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsListTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsListTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsListTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsListTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsItalicMetadata]):
        list_items (Optional[list['ListAllEnvelopeRecipientsTabsListTabsListItemsArrayItemRef']]):
        list_selected_value (Optional[str]):  Example: string.
        list_selected_value_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsListSelectedValueMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsListTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsLockedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsListTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsListTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsListTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsListTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsListTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsHeightMetadata"] = (
        Field(alias="heightMetadata", default=None)
    )
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsItalicMetadata"] = (
        Field(alias="italicMetadata", default=None)
    )
    list_items: Optional[
        list["ListAllEnvelopeRecipientsTabsListTabsListItemsArrayItemRef"]
    ] = Field(alias="listItems", default=None)
    list_selected_value: Optional[str] = Field(alias="listSelectedValue", default=None)
    list_selected_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsListSelectedValueMetadata"
    ] = Field(alias="listSelectedValueMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsListTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsLockedMetadata"] = (
        Field(alias="lockedMetadata", default=None)
    )
    merge_field: Optional["ListAllEnvelopeRecipientsTabsListTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsSharedMetadata"] = (
        Field(alias="sharedMetadata", default=None)
    )
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsStatusMetadata"] = (
        Field(alias="statusMetadata", default=None)
    )
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsListTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsListTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsListTabsArrayItemRef"],
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
