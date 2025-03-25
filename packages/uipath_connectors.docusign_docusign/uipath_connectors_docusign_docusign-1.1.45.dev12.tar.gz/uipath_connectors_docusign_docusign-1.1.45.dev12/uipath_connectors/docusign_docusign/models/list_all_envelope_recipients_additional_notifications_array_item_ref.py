from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_additional_notifications_phone_number import (
    ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumber,
)
from ..models.list_all_envelope_recipients_additional_notifications_secondary_delivery_method_metadata import (
    ListAllEnvelopeRecipientsAdditionalNotificationsSecondaryDeliveryMethodMetadata,
)


class ListAllEnvelopeRecipientsAdditionalNotificationsArrayItemRef(BaseModel):
    """
    Attributes:
        phone_number (Optional[ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumber]):
        secondary_delivery_method (Optional[str]):  Example: string.
        secondary_delivery_method_metadata
                (Optional[ListAllEnvelopeRecipientsAdditionalNotificationsSecondaryDeliveryMethodMetadata]):
        secondary_delivery_status (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    phone_number: Optional[
        "ListAllEnvelopeRecipientsAdditionalNotificationsPhoneNumber"
    ] = Field(alias="phoneNumber", default=None)
    secondary_delivery_method: Optional[str] = Field(
        alias="secondaryDeliveryMethod", default=None
    )
    secondary_delivery_method_metadata: Optional[
        "ListAllEnvelopeRecipientsAdditionalNotificationsSecondaryDeliveryMethodMetadata"
    ] = Field(alias="secondaryDeliveryMethodMetadata", default=None)
    secondary_delivery_status: Optional[str] = Field(
        alias="secondaryDeliveryStatus", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsAdditionalNotificationsArrayItemRef"],
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
