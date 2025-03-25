from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_form_data_response_form_data_array_item_ref import (
    GetFormDataResponseFormDataArrayItemRef,
)
from ..models.get_form_data_response_prefill_form_data import (
    GetFormDataResponsePrefillFormData,
)
from ..models.get_form_data_response_recipient_form_data_array_item_ref import (
    GetFormDataResponseRecipientFormDataArrayItemRef,
)


class GetFormDataResponse(BaseModel):
    """
    Attributes:
        email_subject (Optional[str]):
        envelope_id (Optional[str]): Type the name or ID of the envelope. If the envelope is not found in the drop-down,
                you can first scroll the drop-down till the bottom to get all the available envelopes and then type the envelope
                or retrieve the envelope ID from the DocuSign application -> "Manage" tab -> Goto “Sent” or “Draft” under
                “Envelopes” -> Click on the respective envelope and retrieve the envelope ID from URL. For example, if the URL
                is “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the envelope ID is
                “3ae67e54-f761-4a5b-a23e-b5e4835492cc”
        form_data (Optional[list['GetFormDataResponseFormDataArrayItemRef']]):
        prefill_form_data (Optional[GetFormDataResponsePrefillFormData]):
        recipient_form_data (Optional[list['GetFormDataResponseRecipientFormDataArrayItemRef']]):
        sent_date_time (Optional[str]):
        status (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    email_subject: Optional[str] = Field(alias="emailSubject", default=None)
    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)
    form_data: Optional[list["GetFormDataResponseFormDataArrayItemRef"]] = Field(
        alias="formData", default=None
    )
    prefill_form_data: Optional["GetFormDataResponsePrefillFormData"] = Field(
        alias="prefillFormData", default=None
    )
    recipient_form_data: Optional[
        list["GetFormDataResponseRecipientFormDataArrayItemRef"]
    ] = Field(alias="recipientFormData", default=None)
    sent_date_time: Optional[str] = Field(alias="sentDateTime", default=None)
    status: Optional[str] = Field(alias="status", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetFormDataResponse"], src_dict: Dict[str, Any]):
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
