from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListAllEnvelopeRecipientsIdCheckInformationInputAddressInformationInputAddressInformation(
    BaseModel
):
    """
    Attributes:
        address1 (Optional[str]):  Example: string.
        address2 (Optional[str]):  Example: string.
        city (Optional[str]):  Example: string.
        country (Optional[str]):  Example: string.
        fax (Optional[str]):  Example: string.
        phone (Optional[str]):  Example: string.
        postal_code (Optional[str]):  Example: string.
        state_or_province (Optional[str]):  Example: string.
        zip_plus_4 (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address1: Optional[str] = Field(alias="address1", default=None)
    address2: Optional[str] = Field(alias="address2", default=None)
    city: Optional[str] = Field(alias="city", default=None)
    country: Optional[str] = Field(alias="country", default=None)
    fax: Optional[str] = Field(alias="fax", default=None)
    phone: Optional[str] = Field(alias="phone", default=None)
    postal_code: Optional[str] = Field(alias="postalCode", default=None)
    state_or_province: Optional[str] = Field(alias="stateOrProvince", default=None)
    zip_plus_4: Optional[str] = Field(alias="zipPlus4", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListAllEnvelopeRecipientsIdCheckInformationInputAddressInformationInputAddressInformation"
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
