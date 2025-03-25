from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_name_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsNameMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_optional_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsOptionalMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_scale_value_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsScaleValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsInitialHereTabsArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsFormPageNumberMetadata]):
        hand_draw_required (Optional[str]):  Example: string.
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsHeightMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsNameMetadata]):
        optional (Optional[str]):  Example: string.
        optional_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsOptionalMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsRecipientIdMetadata]):
        scale_value (Optional[str]):  Example: string.
        scale_value_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsScaleValueMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsTabIdMetadata]):
        tab_label (Optional[str]):  Example: string.
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsInitialHereTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    hand_draw_required: Optional[str] = Field(alias="handDrawRequired", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsHeightMetadata"
    ] = Field(alias="heightMetadata", default=None)
    merge_field: Optional["ListAllEnvelopeRecipientsTabsInitialHereTabsMergeField"] = (
        Field(alias="mergeField", default=None)
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsNameMetadata"
    ] = Field(alias="nameMetadata", default=None)
    optional: Optional[str] = Field(alias="optional", default=None)
    optional_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsOptionalMetadata"
    ] = Field(alias="optionalMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    scale_value: Optional[str] = Field(alias="scaleValue", default=None)
    scale_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsScaleValueMetadata"
    ] = Field(alias="scaleValueMetadata", default=None)
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_label: Optional[str] = Field(alias="tabLabel", default=None)
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsWidthMetadata"
    ] = Field(alias="widthMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsInitialHereTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsInitialHereTabsArrayItemRef"],
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
