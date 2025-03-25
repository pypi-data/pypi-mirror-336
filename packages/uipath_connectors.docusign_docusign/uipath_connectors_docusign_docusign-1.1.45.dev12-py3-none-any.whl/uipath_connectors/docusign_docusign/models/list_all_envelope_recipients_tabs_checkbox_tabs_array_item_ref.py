from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_selected_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsSelectedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCheckboxTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsBoldMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsItalicMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsLockedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsRecipientIdMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsRequiredMetadata]):
        selected (Optional[str]):  Example: string.
        selected_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsSelectedMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsUnderlineMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCheckboxTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsCheckboxTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsCheckboxTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsCheckboxTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsCheckboxTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsCheckboxTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    selected: Optional[str] = Field(alias="selected", default=None)
    selected_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsSelectedMetadata"
    ] = Field(alias="selectedMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCheckboxTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCheckboxTabsArrayItemRef"],
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
