from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_identity_verification_input_options_phone_number_list_array_item_ref import (
    ListAllEnvelopeRecipientsIdentityVerificationInputOptionsPhoneNumberListArrayItemRef,
)


class ListAllEnvelopeRecipientsIdentityVerificationInputOptionsArrayItemRef(BaseModel):
    """
    Attributes:
        name (Optional[str]):  Example: string.
        phone_number_list
                (Optional[list['ListAllEnvelopeRecipientsIdentityVerificationInputOptionsPhoneNumberListArrayItemRef']]):
        value_type (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: Optional[str] = Field(alias="name", default=None)
    phone_number_list: Optional[
        list[
            "ListAllEnvelopeRecipientsIdentityVerificationInputOptionsPhoneNumberListArrayItemRef"
        ]
    ] = Field(alias="phoneNumberList", default=None)
    value_type: Optional[str] = Field(alias="valueType", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListAllEnvelopeRecipientsIdentityVerificationInputOptionsArrayItemRef"
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
