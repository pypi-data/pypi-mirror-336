from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsSignHereTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsSignHereTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_optional_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsOptionalMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_scale_value_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsScaleValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsSignHereTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_stamp import (
    ListAllEnvelopeRecipientsTabsSignHereTabsStamp,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_stamp_type_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsStampTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsSignHereTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsSignHereTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsFormPageNumberMetadata]):
        hand_draw_required (Optional[str]):  Example: string.
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsHeightMetadata]):
        is_seal_sign_tab (Optional[str]):  Example: string.
        merge_field (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsNameMetadata]):
        optional (Optional[str]):  Example: string.
        optional_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsOptionalMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsRecipientIdMetadata]):
        scale_value (Optional[str]):  Example: string.
        scale_value_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsScaleValueMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        stamp (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsStamp]):
        stamp_type (Optional[str]):  Example: string.
        stamp_type_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsStampTypeMetadata]):
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsSignHereTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    hand_draw_required: Optional[str] = Field(alias="handDrawRequired", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    is_seal_sign_tab: Optional[str] = Field(alias="isSealSignTab", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsSignHereTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsTabsSignHereTabsNameMetadata"] = (
        Field(alias="nameMetadata", default=None)
    )
    optional: Optional[str] = Field(alias="optional", default=None)
    optional_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsOptionalMetadata"
    ] = Field(alias="optionalMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    scale_value: Optional[str] = Field(alias="scaleValue", default=None)
    scale_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsScaleValueMetadata"
    ] = Field(alias="scaleValueMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    stamp: Optional["ListAllEnvelopeRecipientsTabsSignHereTabsStamp"] = Field(
        alias="stamp", default=None
    )
    stamp_type: Optional[str] = Field(alias="stampType", default=None)
    stamp_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsStampTypeMetadata"
    ] = Field(alias="stampTypeMetadata", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsSignHereTabsArrayItemRef"],
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
