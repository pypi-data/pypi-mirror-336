from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCommissionExpirationTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRequiredMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCommissionExpirationTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsLocalePolicy"
    ] = Field(alias="localePolicy", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCommissionExpirationTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCommissionExpirationTabsArrayItemRef"],
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
