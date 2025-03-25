from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_bold_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_error_details import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_font_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_italic_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_locked_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_required_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_selected_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosSelectedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_status_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_underline_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_value_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs_radio_group_tabs_radios_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosArrayItemRef(
    BaseModel
):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabs
                RadiosAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata
                (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosBoldMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontSizeMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosItalicMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosLockedMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosPageNumberMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosRequiredMetadata]):
        selected (Optional[str]):  Example: string.
        selected_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosSelectedMetadata]):
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosStatusMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosTabIdMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosTabOrderMetadata]):
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosValueMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    selected: Optional[str] = Field(alias="selected", default=None)
    selected_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosSelectedMetadata"
    ] = Field(alias="selectedMetadata", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListAllEnvelopeRecipientsTabsPrefillTabsRadioGroupTabsRadiosArrayItemRef"
        ],
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
