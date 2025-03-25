from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_scale_value_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsScaleValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsNotarySealTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsHeightMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsNameMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsRecipientIdMetadata]):
        scale_value (Optional[str]):  Example: string.
        scale_value_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsScaleValueMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarySealTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsNotarySealTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    scale_value: Optional[str] = Field(alias="scaleValue", default=None)
    scale_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsScaleValueMetadata"
    ] = Field(alias="scaleValueMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarySealTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsNotarySealTabsArrayItemRef"],
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
