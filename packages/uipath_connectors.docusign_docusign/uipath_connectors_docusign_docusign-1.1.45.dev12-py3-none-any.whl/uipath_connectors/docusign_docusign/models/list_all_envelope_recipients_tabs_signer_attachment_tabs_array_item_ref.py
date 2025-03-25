from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_optional_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsOptionalMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_scale_value_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsScaleValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsSignerAttachmentTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormPageNumberMetadata]):
        hand_draw_required (Optional[str]):  Example: string.
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsHeightMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsNameMetadata]):
        optional (Optional[str]):  Example: string.
        optional_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsOptionalMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsRecipientIdMetadata]):
        scale_value (Optional[str]):  Example: string.
        scale_value_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsScaleValueMetadata]):
        smart_contract_information
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    hand_draw_required: Optional[str] = Field(alias="handDrawRequired", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    merge_field: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeField"
    ] = Field(alias="mergeField", default=None)
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    optional: Optional[str] = Field(alias="optional", default=None)
    optional_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsOptionalMetadata"
    ] = Field(alias="optionalMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    scale_value: Optional[str] = Field(alias="scaleValue", default=None)
    scale_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsScaleValueMetadata"
    ] = Field(alias="scaleValueMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsSignerAttachmentTabsArrayItemRef"],
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
