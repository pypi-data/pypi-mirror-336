from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsTitleTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsTitleTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsTitleTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsTitleTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsTitleTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsTitleTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTitleTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTitleTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsTitleTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsTitleTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsTitleTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsTitleTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsRequiredMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsTitleTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsTitleTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsTitleTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsTitleTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsTitleTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsTitleTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsTitleTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsTitleTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsTitleTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsTitleTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsTitleTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsTitleTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsTitleTabsArrayItemRef"],
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
