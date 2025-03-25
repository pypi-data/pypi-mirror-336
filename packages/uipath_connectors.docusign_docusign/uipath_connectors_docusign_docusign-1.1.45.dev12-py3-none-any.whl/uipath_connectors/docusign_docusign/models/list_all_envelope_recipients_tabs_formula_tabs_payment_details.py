from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_formula_tabs_payment_details_currency_code_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsCurrencyCodeMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_payment_details_gateway_account_id_metadata import (
    ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsGatewayAccountIdMetadata,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_payment_details_line_items_array_item_ref import (
    ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsLineItemsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_payment_details_signer_values import (
    ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsSignerValues,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_payment_details_total import (
    ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsTotal,
)


class ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetails(BaseModel):
    """
    Attributes:
        allowed_payment_methods (Optional[list[str]]):
        charge_id (Optional[str]):  Example: string.
        currency_code (Optional[str]):  Example: string.
        currency_code_metadata (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsCurrencyCodeMetadata]):
        custom_metadata (Optional[str]):  Example: string.
        custom_metadata_required (Optional[bool]):  Example: True.
        customer_id (Optional[str]):  Example: string.
        gateway_account_id (Optional[str]):  Example: string.
        gateway_account_id_metadata
                (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsGatewayAccountIdMetadata]):
        gateway_display_name (Optional[str]):  Example: string.
        gateway_name (Optional[str]):  Example: string.
        line_items (Optional[list['ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsLineItemsArrayItemRef']]):
        payment_option (Optional[str]):  Example: string.
        payment_source_id (Optional[str]):  Example: string.
        signer_values (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsSignerValues]):
        status (Optional[str]):  Example: string.
        total (Optional[ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsTotal]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    allowed_payment_methods: Optional[list[str]] = Field(
        alias="allowedPaymentMethods", default=None
    )
    charge_id: Optional[str] = Field(alias="chargeId", default=None)
    currency_code: Optional[str] = Field(alias="currencyCode", default=None)
    currency_code_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsCurrencyCodeMetadata"
    ] = Field(alias="currencyCodeMetadata", default=None)
    custom_metadata: Optional[str] = Field(alias="customMetadata", default=None)
    custom_metadata_required: Optional[bool] = Field(
        alias="customMetadataRequired", default=None
    )
    customer_id: Optional[str] = Field(alias="customerId", default=None)
    gateway_account_id: Optional[str] = Field(alias="gatewayAccountId", default=None)
    gateway_account_id_metadata: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsGatewayAccountIdMetadata"
    ] = Field(alias="gatewayAccountIdMetadata", default=None)
    gateway_display_name: Optional[str] = Field(
        alias="gatewayDisplayName", default=None
    )
    gateway_name: Optional[str] = Field(alias="gatewayName", default=None)
    line_items: Optional[
        list[
            "ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsLineItemsArrayItemRef"
        ]
    ] = Field(alias="lineItems", default=None)
    payment_option: Optional[str] = Field(alias="paymentOption", default=None)
    payment_source_id: Optional[str] = Field(alias="paymentSourceId", default=None)
    signer_values: Optional[
        "ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsSignerValues"
    ] = Field(alias="signerValues", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    total: Optional["ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetailsTotal"] = (
        Field(alias="total", default=None)
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsTabsFormulaTabsPaymentDetails"],
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
