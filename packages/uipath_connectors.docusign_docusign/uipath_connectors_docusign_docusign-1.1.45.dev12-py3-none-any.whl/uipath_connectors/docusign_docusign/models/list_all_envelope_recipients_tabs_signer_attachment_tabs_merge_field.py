from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field_allow_sender_to_edit_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldAllowSenderToEditMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field_configuration_type_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldConfigurationTypeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field_path_extended_array_item_ref import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathExtendedArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field_path_extended_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathExtendedMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field_path_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field_row_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldRowMetadata,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_merge_field_write_back_metadata import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldWriteBackMetadata,
)


class ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeField(BaseModel):
    """
    Attributes:
        allow_sender_to_edit (Optional[str]):  Example: string.
        allow_sender_to_edit_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldAllowSenderToEditMetadata]):
        configuration_type (Optional[str]):  Example: string.
        configuration_type_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldConfigurationTypeMetadata]):
        path (Optional[str]):  Example: string.
        path_extended
                (Optional[list['ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathExtendedArrayItemRef']]):
        path_extended_metadata
                (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathExtendedMetadata]):
        path_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathMetadata]):
        row (Optional[str]):  Example: string.
        row_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldRowMetadata]):
        write_back (Optional[str]):  Example: string.
        write_back_metadata (Optional[ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldWriteBackMetadata]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    allow_sender_to_edit: Optional[str] = Field(alias="allowSenderToEdit", default=None)
    allow_sender_to_edit_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldAllowSenderToEditMetadata"
    ] = Field(alias="allowSenderToEditMetadata", default=None)
    configuration_type: Optional[str] = Field(alias="configurationType", default=None)
    configuration_type_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldConfigurationTypeMetadata"
    ] = Field(alias="configurationTypeMetadata", default=None)
    path: Optional[str] = Field(alias="path", default=None)
    path_extended: Optional[
        list[
            "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathExtendedArrayItemRef"
        ]
    ] = Field(alias="pathExtended", default=None)
    path_extended_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathExtendedMetadata"
    ] = Field(alias="pathExtendedMetadata", default=None)
    path_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldPathMetadata"
    ] = Field(alias="pathMetadata", default=None)
    row: Optional[str] = Field(alias="row", default=None)
    row_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldRowMetadata"
    ] = Field(alias="rowMetadata", default=None)
    write_back: Optional[str] = Field(alias="writeBack", default=None)
    write_back_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeFieldWriteBackMetadata"
    ] = Field(alias="writeBackMetadata", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsSignerAttachmentTabsMergeField"],
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
