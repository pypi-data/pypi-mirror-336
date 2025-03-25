from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_envelope_response_folders_error_details import (
    GetEnvelopeResponseFoldersErrorDetails,
)
from ..models.get_envelope_response_folders_filter import (
    GetEnvelopeResponseFoldersFilter,
)
from ..models.get_envelope_response_folders_folder_items_array_item_ref import (
    GetEnvelopeResponseFoldersFolderItemsArrayItemRef,
)
from ..models.get_envelope_response_folders_folders_array_item_ref import (
    GetEnvelopeResponseFoldersFoldersArrayItemRef,
)
from ..models.get_envelope_response_folders_owner import GetEnvelopeResponseFoldersOwner


class GetEnvelopeResponseFoldersArrayItemRef(BaseModel):
    """
    Attributes:
        error_details (Optional[GetEnvelopeResponseFoldersErrorDetails]):
        filter_ (Optional[GetEnvelopeResponseFoldersFilter]):
        folder_id (Optional[str]):
        folder_items (Optional[list['GetEnvelopeResponseFoldersFolderItemsArrayItemRef']]):
        folders (Optional[list['GetEnvelopeResponseFoldersFoldersArrayItemRef']]):
        has_access (Optional[str]):
        has_sub_folders (Optional[str]):
        item_count (Optional[str]):
        name (Optional[str]):
        owner (Optional[GetEnvelopeResponseFoldersOwner]):
        parent_folder_id (Optional[str]):
        parent_folder_uri (Optional[str]):
        sub_folder_count (Optional[str]):
        type_ (Optional[str]):
        uri (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    error_details: Optional["GetEnvelopeResponseFoldersErrorDetails"] = Field(
        alias="errorDetails", default=None
    )
    filter_: Optional["GetEnvelopeResponseFoldersFilter"] = Field(
        alias="filter", default=None
    )
    folder_id: Optional[str] = Field(alias="folderId", default=None)
    folder_items: Optional[
        list["GetEnvelopeResponseFoldersFolderItemsArrayItemRef"]
    ] = Field(alias="folderItems", default=None)
    folders: Optional[list["GetEnvelopeResponseFoldersFoldersArrayItemRef"]] = Field(
        alias="folders", default=None
    )
    has_access: Optional[str] = Field(alias="hasAccess", default=None)
    has_sub_folders: Optional[str] = Field(alias="hasSubFolders", default=None)
    item_count: Optional[str] = Field(alias="itemCount", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    owner: Optional["GetEnvelopeResponseFoldersOwner"] = Field(
        alias="owner", default=None
    )
    parent_folder_id: Optional[str] = Field(alias="parentFolderId", default=None)
    parent_folder_uri: Optional[str] = Field(alias="parentFolderUri", default=None)
    sub_folder_count: Optional[str] = Field(alias="subFolderCount", default=None)
    type_: Optional[str] = Field(alias="type", default=None)
    uri: Optional[str] = Field(alias="uri", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseFoldersArrayItemRef"], src_dict: Dict[str, Any]
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
