from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsSsnTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsSsnTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsSsnTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_require_all_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsRequireAllMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_require_initial_on_shared_change_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsRequireInitialOnSharedChangeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_sender_required_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsSenderRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsSsnTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_validation_message_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsValidationMessageMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_validation_pattern_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsValidationPatternMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsSsnTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsSsnTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsSsnTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsSsnTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsSsnTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsRecipientIdMetadata]):
        require_all (Optional[str]):  Example: string.
        require_all_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsRequireAllMetadata]):
        require_initial_on_shared_change (Optional[str]):  Example: string.
        require_initial_on_shared_change_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSsnTabsRequireInitialOnSharedChangeMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsRequiredMetadata]):
        sender_required (Optional[str]):  Example: string.
        sender_required_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsSenderRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsSsnTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsUnderlineMetadata]):
        validation_message (Optional[str]):  Example: string.
        validation_message_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsValidationMessageMetadata]):
        validation_pattern (Optional[str]):  Example: string.
        validation_pattern_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsValidationPatternMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSsnTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsBoldMetadata"] = Field(
        alias="boldMetadata", default=None
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsSsnTabsErrorDetails"] = Field(
        alias="errorDetails", default=None
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsFontMetadata"] = Field(
        alias="fontMetadata", default=None
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsHeightMetadata"] = (
        Field(alias="heightMetadata", default=None)
    )
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsItalicMetadata"] = (
        Field(alias="italicMetadata", default=None)
    )
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsSsnTabsLocalePolicy"] = Field(
        alias="localePolicy", default=None
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsLockedMetadata"] = (
        Field(alias="lockedMetadata", default=None)
    )
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsSsnTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsNameMetadata"] = Field(
        alias="nameMetadata", default=None
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    require_all: Optional[str] = Field(alias="requireAll", default=None)
    require_all_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsRequireAllMetadata"
    ] = Field(alias="requireAllMetadata", default=None)
    require_initial_on_shared_change: Optional[str] = Field(
        alias="requireInitialOnSharedChange", default=None
    )
    require_initial_on_shared_change_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsRequireInitialOnSharedChangeMetadata"
    ] = Field(alias="requireInitialOnSharedChangeMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    sender_required: Optional[str] = Field(alias="senderRequired", default=None)
    sender_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsSenderRequiredMetadata"
    ] = Field(alias="senderRequiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsSharedMetadata"] = (
        Field(alias="sharedMetadata", default=None)
    )
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsStatusMetadata"] = (
        Field(alias="statusMetadata", default=None)
    )
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    validation_message: Optional[str] = Field(alias="validationMessage", default=None)
    validation_message_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsValidationMessageMetadata"
    ] = Field(alias="validationMessageMetadata", default=None)
    validation_pattern: Optional[str] = Field(alias="validationPattern", default=None)
    validation_pattern_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsValidationPatternMetadata"
    ] = Field(alias="validationPatternMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsValueMetadata"] = (
        Field(alias="valueMetadata", default=None)
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsSsnTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSsnTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsSsnTabsArrayItemRef"],
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
