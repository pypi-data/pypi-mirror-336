from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCurrencyTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsNameMetadata]):
        numerical_value (Optional[str]):  Example: string.
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCurrencyTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsCurrencyTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsCurrencyTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsCurrencyTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsCurrencyTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsCurrencyTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsCurrencyTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    numerical_value: Optional[str] = Field(alias="numericalValue", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsSharedMetadata"
    ] = Field(alias="sharedMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCurrencyTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCurrencyTabsArrayItemRef"],
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
