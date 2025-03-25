from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCommissionCountyTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsRequiredMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionCountyTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionCountyTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCommissionCountyTabsArrayItemRef"],
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
