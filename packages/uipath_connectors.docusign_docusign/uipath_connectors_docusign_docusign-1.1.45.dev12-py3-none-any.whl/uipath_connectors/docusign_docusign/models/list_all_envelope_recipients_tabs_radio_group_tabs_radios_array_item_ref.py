from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_allow_white_space_in_characters_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorAllowWhiteSpaceInCharactersMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_case_sensitive_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorCaseSensitiveMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_horizontal_alignment_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorHorizontalAlignmentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_ignore_if_not_present_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorIgnoreIfNotPresentMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_match_whole_word_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorMatchWholeWordMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_string_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorStringMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_tab_processor_version_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorTabProcessorVersionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_units_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorUnitsMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_x_offset_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorXOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_anchor_y_offset_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorYOffsetMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_bold_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosBoldMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_error_details import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosErrorDetails,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_font_color_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontColorMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_font_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_font_size_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontSizeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_italic_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosItalicMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_locked_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosLockedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_page_number_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosPageNumberMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_required_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosRequiredMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_selected_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosSelectedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_status_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosStatusMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_tab_id_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosTabIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_tab_order_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosTabOrderMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_underline_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosUnderlineMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_value_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosValueMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_x_position_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosXPositionMetadata,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_radios_y_position_metadata import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosYPositionMetadata,
)


class ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosArrayItemRef(BaseModel):
    """
    Attributes:
        anchor_allow_white_space_in_characters (Optional[str]):  Example: string.
        anchor_allow_white_space_in_characters_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorAllowWhiteSpaceInCharactersMetadata]):
        anchor_case_sensitive (Optional[str]):  Example: string.
        anchor_case_sensitive_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorCaseSensitiveMetadata]):
        anchor_horizontal_alignment (Optional[str]):  Example: string.
        anchor_horizontal_alignment_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorHorizontalAlignmentMetadata]):
        anchor_ignore_if_not_present (Optional[str]):  Example: string.
        anchor_ignore_if_not_present_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorIgnoreIfNotPresentMetadata]):
        anchor_match_whole_word (Optional[str]):  Example: string.
        anchor_match_whole_word_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorMatchWholeWordMetadata]):
        anchor_string (Optional[str]):  Example: string.
        anchor_string_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorStringMetadata]):
        anchor_tab_processor_version (Optional[str]):  Example: string.
        anchor_tab_processor_version_metadata
                (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorTabProcessorVersionMetadata]):
        anchor_units (Optional[str]):  Example: string.
        anchor_units_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorUnitsMetadata]):
        anchor_x_offset (Optional[str]):  Example: string.
        anchor_x_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorXOffsetMetadata]):
        anchor_y_offset (Optional[str]):  Example: string.
        anchor_y_offset_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorYOffsetMetadata]):
        bold (Optional[str]):  Example: string.
        bold_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosBoldMetadata]):
        error_details (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosErrorDetails]):
        font (Optional[str]):  Example: string.
        font_color (Optional[str]):  Example: string.
        font_color_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontColorMetadata]):
        font_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontMetadata]):
        font_size (Optional[str]):  Example: string.
        font_size_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontSizeMetadata]):
        italic (Optional[str]):  Example: string.
        italic_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosItalicMetadata]):
        locked (Optional[str]):  Example: string.
        locked_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosLockedMetadata]):
        page_number (Optional[str]):  Example: string.
        page_number_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosPageNumberMetadata]):
        required (Optional[str]):  Example: string.
        required_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosRequiredMetadata]):
        selected (Optional[str]):  Example: string.
        selected_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosSelectedMetadata]):
        status (Optional[str]):  Example: string.
        status_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosStatusMetadata]):
        tab_id (Optional[str]):  Example: string.
        tab_id_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosTabIdMetadata]):
        tab_order (Optional[str]):  Example: string.
        tab_order_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosTabOrderMetadata]):
        underline (Optional[str]):  Example: string.
        underline_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosUnderlineMetadata]):
        value (Optional[str]):  Example: string.
        value_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosValueMetadata]):
        x_position (Optional[str]):  Example: string.
        x_position_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosXPositionMetadata]):
        y_position (Optional[str]):  Example: string.
        y_position_metadata (Optional[ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosYPositionMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anchor_allow_white_space_in_characters: Optional[str] = Field(
        alias="anchorAllowWhiteSpaceInCharacters", default=None
    )
    anchor_allow_white_space_in_characters_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorAllowWhiteSpaceInCharactersMetadata"
    ] = Field(alias="anchorAllowWhiteSpaceInCharactersMetadata", default=None)
    anchor_case_sensitive: Optional[str] = Field(
        alias="anchorCaseSensitive", default=None
    )
    anchor_case_sensitive_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorCaseSensitiveMetadata"
    ] = Field(alias="anchorCaseSensitiveMetadata", default=None)
    anchor_horizontal_alignment: Optional[str] = Field(
        alias="anchorHorizontalAlignment", default=None
    )
    anchor_horizontal_alignment_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorHorizontalAlignmentMetadata"
    ] = Field(alias="anchorHorizontalAlignmentMetadata", default=None)
    anchor_ignore_if_not_present: Optional[str] = Field(
        alias="anchorIgnoreIfNotPresent", default=None
    )
    anchor_ignore_if_not_present_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorIgnoreIfNotPresentMetadata"
    ] = Field(alias="anchorIgnoreIfNotPresentMetadata", default=None)
    anchor_match_whole_word: Optional[str] = Field(
        alias="anchorMatchWholeWord", default=None
    )
    anchor_match_whole_word_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorMatchWholeWordMetadata"
    ] = Field(alias="anchorMatchWholeWordMetadata", default=None)
    anchor_string: Optional[str] = Field(alias="anchorString", default=None)
    anchor_string_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorStringMetadata"
    ] = Field(alias="anchorStringMetadata", default=None)
    anchor_tab_processor_version: Optional[str] = Field(
        alias="anchorTabProcessorVersion", default=None
    )
    anchor_tab_processor_version_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorTabProcessorVersionMetadata"
    ] = Field(alias="anchorTabProcessorVersionMetadata", default=None)
    anchor_units: Optional[str] = Field(alias="anchorUnits", default=None)
    anchor_units_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorUnitsMetadata"
    ] = Field(alias="anchorUnitsMetadata", default=None)
    anchor_x_offset: Optional[str] = Field(alias="anchorXOffset", default=None)
    anchor_x_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorXOffsetMetadata"
    ] = Field(alias="anchorXOffsetMetadata", default=None)
    anchor_y_offset: Optional[str] = Field(alias="anchorYOffset", default=None)
    anchor_y_offset_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosAnchorYOffsetMetadata"
    ] = Field(alias="anchorYOffsetMetadata", default=None)
    bold: Optional[str] = Field(alias="bold", default=None)
    bold_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosBoldMetadata"
    ] = Field(alias="boldMetadata", default=None)
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    font: Optional[str] = Field(alias="font", default=None)
    font_color: Optional[str] = Field(alias="fontColor", default=None)
    font_color_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontColorMetadata"
    ] = Field(alias="fontColorMetadata", default=None)
    font_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontMetadata"
    ] = Field(alias="fontMetadata", default=None)
    font_size: Optional[str] = Field(alias="fontSize", default=None)
    font_size_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosFontSizeMetadata"
    ] = Field(alias="fontSizeMetadata", default=None)
    italic: Optional[str] = Field(alias="italic", default=None)
    italic_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosItalicMetadata"
    ] = Field(alias="italicMetadata", default=None)
    locked: Optional[str] = Field(alias="locked", default=None)
    locked_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosLockedMetadata"
    ] = Field(alias="lockedMetadata", default=None)
    page_number: Optional[str] = Field(alias="pageNumber", default=None)
    page_number_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosPageNumberMetadata"
    ] = Field(alias="pageNumberMetadata", default=None)
    required: Optional[str] = Field(alias="required", default=None)
    required_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosRequiredMetadata"
    ] = Field(alias="requiredMetadata", default=None)
    selected: Optional[str] = Field(alias="selected", default=None)
    selected_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosSelectedMetadata"
    ] = Field(alias="selectedMetadata", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosStatusMetadata"
    ] = Field(alias="statusMetadata", default=None)
    tab_id: Optional[str] = Field(alias="tabId", default=None)
    tab_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosTabIdMetadata"
    ] = Field(alias="tabIdMetadata", default=None)
    tab_order: Optional[str] = Field(alias="tabOrder", default=None)
    tab_order_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosTabOrderMetadata"
    ] = Field(alias="tabOrderMetadata", default=None)
    underline: Optional[str] = Field(alias="underline", default=None)
    underline_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosUnderlineMetadata"
    ] = Field(alias="underlineMetadata", default=None)
    value: Optional[str] = Field(alias="value", default=None)
    value_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosValueMetadata"
    ] = Field(alias="valueMetadata", default=None)
    x_position: Optional[str] = Field(alias="xPosition", default=None)
    x_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosXPositionMetadata"
    ] = Field(alias="xPositionMetadata", default=None)
    y_position: Optional[str] = Field(alias="yPosition", default=None)
    y_position_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosYPositionMetadata"
    ] = Field(alias="yPositionMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsRadioGroupTabsRadiosArrayItemRef"],
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
