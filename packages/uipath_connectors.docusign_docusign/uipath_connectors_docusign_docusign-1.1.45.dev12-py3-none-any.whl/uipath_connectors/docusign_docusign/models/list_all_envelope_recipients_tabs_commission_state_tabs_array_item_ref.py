from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCommissionStateTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsRequiredMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionStateTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionStateTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCommissionStateTabsArrayItemRef"],
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
