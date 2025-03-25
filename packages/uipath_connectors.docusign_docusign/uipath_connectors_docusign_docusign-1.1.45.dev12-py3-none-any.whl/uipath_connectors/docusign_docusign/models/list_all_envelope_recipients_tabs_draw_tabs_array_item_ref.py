from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_conditional_parent_label_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsConditionalParentLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_conditional_parent_value_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsConditionalParentValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_custom_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsCustomTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_document_id_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsDocumentIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_error_details import (
    ListAllEnvelopeRecipientsTabsDrawTabsErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_form_order_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsFormOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_form_page_label_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsFormPageLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_form_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsFormPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_height_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsHeightMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_locked_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_merge_field import (
    ListAllEnvelopeRecipientsTabsDrawTabsMergeField,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_recipient_id_guid_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsRecipientIdGuidMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_recipient_id_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsRecipientIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_required_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_shared_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsSharedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_smart_contract_information import (
    ListAllEnvelopeRecipientsTabsDrawTabsSmartContractInformation,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_status_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_tab_group_labels_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsTabGroupLabelsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_tab_label_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsTabLabelMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_tab_type_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsTabTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_template_locked_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsTemplateLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_template_required_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsTemplateRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_tool_tip_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsToolTipMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_width_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsWidthMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsDrawTabsYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsDrawTabsArrayItemRef(BaseModel):
    """
    Attributes:
        allow_signer_upload (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsAnchorYOffsetMetadata]):
        conditional_parent_label (Optional[str]):  Example: string.
        conditional_parent_label_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDrawTabsConditionalParentLabelMetadata]):
        conditional_parent_value (Optional[str]):  Example: string.
        conditional_parent_value_metadata
                (Optional[ListAllEnvelopeRecipientsTabsDrawTabsConditionalParentValueMetadata]):
        custom_tab_id (Optional[str]):  Example: string.
        custom_tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsCustomTabIdMetadata]):
        document_id (Optional[str]):  Example: string.
        document_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsDocumentIdMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsDrawTabsErrorDetails]):
        form_order (Optional[str]):  Example: string.
        form_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsFormOrderMetadata]):
        form_page_label (Optional[str]):  Example: string.
        form_page_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsFormPageLabelMetadata]):
        form_page_number (Optional[str]):  Example: string.
        form_page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsFormPageNumberMetadata]):
        height (Optional[str]):  Example: string.
        height_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsHeightMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsLockedMetadata]):
        merge_field (Optional[ListAllEnvelopeRecipientsTabsDrawTabsMergeField]):
        merge_field_xml (Optional[str]):  Example: string.
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsPageNumberMetadata]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_id_guid_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsRecipientIdGuidMetadata]):
        recipient_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsRecipientIdMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsRequiredMetadata]):
        shared (Optional[str]):  Example: string.
        shared_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsSharedMetadata]):
        smart_contract_information (Optional[ListAllEnvelopeRecipientsTabsDrawTabsSmartContractInformation]):
        source (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsStatusMetadata]):
        tab_group_labels (Optional[list[str]]):
        tab_group_labels_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsTabGroupLabelsMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsTabIdMetadata]):
        tab_label_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsTabLabelMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsTabOrderMetadata]):
        tab_type (Optional[str]):  Example: string.
        tab_type_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsTabTypeMetadata]):
        template_locked (Optional[str]):  Example: string.
        template_locked_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsTemplateLockedMetadata]):
        template_required (Optional[str]):  Example: string.
        template_required_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsTemplateRequiredMetadata]):
        tool_tip_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsToolTipMetadata]):
        tooltip (Optional[str]):  Example: string.
        use_background_as_canvas (Optional[str]):  Example: string.
        width (Optional[str]):  Example: string.
        width_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsWidthMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsDrawTabsYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    allow_signer_upload: Optional[str] = Field(alias="allowSignerUpload", default=None)
    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    conditional_parent_label: Optional[str] = Field(
        alias="conditionalParentLabel", default=None
    )
    conditional_parent_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsConditionalParentLabelMetadata"
    ] = Field(alias="conditionalParentLabelMetadata", default=None)
    conditional_parent_value: Optional[str] = Field(
        alias="conditionalParentValue", default=None
    )
    conditional_parent_value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsConditionalParentValueMetadata"
    ] = Field(alias="conditionalParentValueMetadata", default=None)
    custom_tab_id: Optional[str] = Field(alias="customTabId", default=None)
    custom_tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsCustomTabIdMetadata"
    ] = Field(alias="customTabIdMetadata", default=None)
    document_id: Optional[str] = Field(alias="documentId", default=None)
    document_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsDocumentIdMetadata"
    ] = Field(alias="documentIdMetadata", default=None)
    error_details: Optional["ListAllEnvelopeRecipientsTabsDrawTabsErrorDetails"] = (
        Field(alias="errorDetails", default=None)
    )
    form_order: Optional[str] = Field(alias="formOrder", default=None)
    form_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsFormOrderMetadata"
    ] = Field(alias="formOrderMetadata", default=None)
    form_page_label: Optional[str] = Field(alias="formPageLabel", default=None)
    form_page_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsFormPageLabelMetadata"
    ] = Field(alias="formPageLabelMetadata", default=None)
    form_page_number: Optional[str] = Field(alias="formPageNumber", default=None)
    form_page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsFormPageNumberMetadata"
    ] = Field(alias="formPageNumberMetadata", default=None)
    height: Optional[str] = Field(alias="height", default=None)
    height_metadata: Optional["ListAllEnvelopeRecipientsTabsDrawTabsHeightMetadata"] = (
        Field(alias="heightMetadata", default=None)
    )
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional["ListAllEnvelopeRecipientsTabsDrawTabsLockedMetadata"] = (
        Field(alias="lockedMetadata", default=None)
    )
    merge_field: Optional["ListAllEnvelopeRecipientsTabsDrawTabsMergeField"] = Field(
        alias="mergeField", default=None
    )
    merge_field_xml: Optional[str] = Field(alias="mergeFieldXml", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_id_guid_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsRecipientIdGuidMetadata"
    ] = Field(alias="recipientIdGuidMetadata", default=None)
    recipient_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsRecipientIdMetadata"
    ] = Field(alias="recipientIdMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    shared: Optional[str] = Field(alias="shared", default=None)
    shared_metadata: Optional["ListAllEnvelopeRecipientsTabsDrawTabsSharedMetadata"] = (
        Field(alias="sharedMetadata", default=None)
    )
    smart_contract_information: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsSmartContractInformation"
    ] = Field(alias="smartContractInformation", default=None)
    source: Optional[str] = Field(alias="source", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional["ListAllEnvelopeRecipientsTabsDrawTabsStatusMetadata"] = (
        Field(alias="statusMetadata", default=None)
    )
    tab_group_labels: Optional[list[str]] = Field(alias="tabGroupLabels", default=None)
    tab_group_labels_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsTabGroupLabelsMetadata"
    ] = Field(alias="tabGroupLabelsMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional["ListAllEnvelopeRecipientsTabsDrawTabsTabIdMetadata"] = (
        Field(alias="tabIdMetadata", default=None)
    )
    tab_label_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsTabLabelMetadata"
    ] = Field(alias="tabLabelMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    tab_type: Optional[str] = Field(alias="tabType", default=None)
    tab_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsTabTypeMetadata"
    ] = Field(alias="tabTypeMetadata", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsTemplateLockedMetadata"
    ] = Field(alias="templateLockedMetadata", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    template_required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsTemplateRequiredMetadata"
    ] = Field(alias="templateRequiredMetadata", default=None)
    tool_tip_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsToolTipMetadata"
    ] = Field(alias="toolTipMetadata", default=None)
    tooltip: Optional[str] = Field(alias="tooltip", default=None)
    use_background_as_canvas: Optional[str] = Field(
        alias="useBackgroundAsCanvas", default=None
    )
    width: Optional[str] = Field(alias="width", default=None)
    width_metadata: Optional["ListAllEnvelopeRecipientsTabsDrawTabsWidthMetadata"] = (
        Field(alias="widthMetadata", default=None)
    )
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsDrawTabsYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsDrawTabsArrayItemRef"],
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
