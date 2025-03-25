from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsNotarizeTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsHeightMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsLockedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsRequiredMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsTabIdMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsNotarizeTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsNotarizeTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsNotarizeTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsNotarizeTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsNotarizeTabsArrayItemRef"],
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
