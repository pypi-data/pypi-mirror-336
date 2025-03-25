from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCommissionNumberTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsRequiredMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionNumberTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionNumberTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCommissionNumberTabsArrayItemRef"],
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
