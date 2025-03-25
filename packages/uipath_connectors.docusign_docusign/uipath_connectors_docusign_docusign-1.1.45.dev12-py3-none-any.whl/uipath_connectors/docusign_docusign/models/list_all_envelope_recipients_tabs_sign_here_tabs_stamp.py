from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_stamp_date_stamp_properties import (
    ListAllEnvelopeRecipientsTabsSignHereTabsStampDateStampProperties,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_stamp_error_details import (
    ListAllEnvelopeRecipientsTabsSignHereTabsStampErrorDetails,
)


class ListAllEnvelopeRecipientsTabsSignHereTabsStamp(BaseModel):
    """
    Attributes:
        adopted_date_time (Optional[str]):  Example: string.
        created_date_time (Optional[str]):  Example: string.
        custom_field (Optional[str]):  Example: string.
        date_stamp_properties (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsStampDateStampProperties]):
        disallow_user_resize_stamp (Optional[str]):  Example: string.
        error_details (Optional[ListAllEnvelopeRecipientsTabsSignHereTabsStampErrorDetails]):
        external_id (Optional[str]):  Example: string.
        image_base_64 (Optional[str]):  Example: string.
        image_type (Optional[str]):  Example: string.
        last_modified_date_time (Optional[str]):  Example: string.
        phonetic_name (Optional[str]):  Example: string.
        signature_name (Optional[str]):  Example: string.
        stamp_format (Optional[str]):  Example: string.
        stamp_image_uri (Optional[str]):  Example: string.
        stamp_size_mm (Optional[str]):  Example: string.
        status (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    adopted_date_time: Optional[str] = Field(alias="adoptedDateTime", default=None)
    created_date_time: Optional[str] = Field(alias="createdDateTime", default=None)
    custom_field: Optional[str] = Field(alias="customField", default=None)
    date_stamp_properties: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsStampDateStampProperties"
    ] = Field(alias="dateStampProperties", default=None)
    disallow_user_resize_stamp: Optional[str] = Field(
        alias="disallowUserResizeStamp", default=None
    )
    error_details: Optional[
        "ListAllEnvelopeRecipientsTabsSignHereTabsStampErrorDetails"
    ] = Field(alias="errorDetails", default=None)
    external_id: Optional[str] = Field(alias="externalID", default=None)
    image_base_64: Optional[str] = Field(alias="imageBase64", default=None)
    image_type: Optional[str] = Field(alias="imageType", default=None)
    last_modified_date_time: Optional[str] = Field(
        alias="lastModifiedDateTime", default=None
    )
    phonetic_name: Optional[str] = Field(alias="phoneticName", default=None)
    signature_name: Optional[str] = Field(alias="signatureName", default=None)
    stamp_format: Optional[str] = Field(alias="stampFormat", default=None)
    stamp_image_uri: Optional[str] = Field(alias="stampImageUri", default=None)
    stamp_size_mm: Optional[str] = Field(alias="stampSizeMM", default=None)
    status: Optional[str] = Field(alias="status", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsSignHereTabsStamp"],
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
