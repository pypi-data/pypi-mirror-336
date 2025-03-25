from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsLineItemsArrayItemRef(
    BaseModel
):
    """
    Attributes:
        amount_reference (Optional[str]):  Example: string.
        description (Optional[str]):  Example: string.
        item_code (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    amount_reference: Optional[str] = Field(alias="amountReference", default=None)
    description: Optional[str] = Field(alias="description", default=None)
    item_code: Optional[str] = Field(alias="itemCode", default=None)
    name: Optional[str] = Field(alias="name", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type[
            "ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsLineItemsArrayItemRef"
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
