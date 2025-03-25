from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_bold_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_conceal_value_on_document_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsConcealValueOnDocumentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_disable_auto_size_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsDisableAutoSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsCompanyTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_font_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_italic_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_locale_policy import (
    ListAllEnvelopeRecipientsTabsCompanyTabsLocalePolicy,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_max_length_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsMaxLengthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsCompanyTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_original_value_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsOriginalValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsCompanyTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_underline_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_value_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsCompanyTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsCompanyTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsBoldMetadata]):
        conceal_value_on_document (Optional[str]):  Example: string.
        conceal_value_on_document_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsConcealValueOnDocumentMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsCustomTabIdMetadata]):
        disable_auto_size (Optional[str]):  Example: string.
        disable_auto_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsDisableAutoSizeMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsFontSizeMetadata]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsHeightMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsItalicMetadata]):
        locale_policy (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsLocalePolicy]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsLockedMetadata]):
        max_length (Optional[str]):  Example: string.
        max_length_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsMaxLengthMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsNameMetadata]):
        original_value (Optional[str]):  Example: string.
        original_value_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsOriginalValueMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsRequiredMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsValueMetadata]):
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsCompanyTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional["ListAllEnvelopeRecipientsTabsCompanyTabsBoldMetadata"] = (
        Field(alias="boldMetadata", default=None)
    )
    conceal_value_on_document: Optional[str] = Field(
        alias="concealValueOnDocument", default=None
    )
    conceal_value_on_document_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsConcealValueOnDocumentMetadata"
    ] = Field(alias="concealValueOnDocumentMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    disable_auto_size: Optional[str] = Field(alias="disableAutoSize", default=None)
    disable_auto_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsDisableAutoSizeMetadata"
    ] = Field(alias="disableAutoSizeMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsCompanyTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional["ListAllEnvelopeRecipientsTabsCompanyTabsFontMetadata"] = (
        Field(alias="fontMetadata", default=None)
    )
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locale_policy: Optional["ListAllEnvelopeRecipientsTabsCompanyTabsLocalePolicy"] = (
        Field(alias="localePolicy", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    max_length: Optional[str] = Field(alias="maxLength", default=None)
    max_length_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsMaxLengthMetadata"
    ] = Field(alias="maxLengthMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsCompanyTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsCompanyTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    original_value: Optional[str] = Field(alias="originalValue", default=None)
    original_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsOriginalValueMetadata"
    ] = Field(alias="originalValueMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsCompanyTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsCompanyTabsArrayItemRef"],
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
