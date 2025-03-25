from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListAllEnvelopeRecipientsTabsNoteTabsLocalePolicy(BaseModel):
    """
    Attributes:
        address_format (Optional[str]):  Example: string.
        calendar_type (Optional[str]):  Example: string.
        culture_name (Optional[str]):  Example: string.
        currency_code (Optional[str]):  Example: string.
        currency_negative_format (Optional[str]):  Example: string.
        currency_positive_format (Optional[str]):  Example: string.
        custom_date_format (Optional[str]):  Example: string.
        custom_time_format (Optional[str]):  Example: string.
        date_format (Optional[str]):  Example: string.
        initial_format (Optional[str]):  Example: string.
        name_format (Optional[str]):  Example: string.
        time_format (Optional[str]):  Example: string.
        time_zone (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address_format: Optional[str] = Field(alias="addressFormat", default=None)
    calendar_type: Optional[str] = Field(alias="calendarType", default=None)
    culture_name: Optional[str] = Field(alias="cultureName", default=None)
    currency_code: Optional[str] = Field(alias="currencyCode", default=None)
    currency_negative_format: Optional[str] = Field(
        alias="currencyNegativeFormat", default=None
    )
    currency_positive_format: Optional[str] = Field(
        alias="currencyPositiveFormat", default=None
    )
    custom_date_format: Optional[str] = Field(alias="customDateFormat", default=None)
    custom_time_format: Optional[str] = Field(alias="customTimeFormat", default=None)
    date_format: Optional[str] = Field(alias="dateFormat", default=None)
    initial_format: Optional[str] = Field(alias="initialFormat", default=None)
    name_format: Optional[str] = Field(alias="nameFormat", default=None)
    time_format: Optional[str] = Field(alias="timeFormat", default=None)
    time_zone: Optional[str] = Field(alias="timeZone", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsNoteTabsLocalePolicy"],
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
