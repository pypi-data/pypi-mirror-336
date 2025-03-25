from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_id_check_information_input_address_information_input import (
    ListAllEnvelopeRecipientsIdCheckInformationInputAddressInformationInput,
)
from ..models.list_all_envelope_recipients_id_check_information_input_dob_information_input import (
    ListAllEnvelopeRecipientsIdCheckInformationInputDobInformationInput,
)
from ..models.list_all_envelope_recipients_id_check_information_input_ssn_4_information_input import (
    ListAllEnvelopeRecipientsIdCheckInformationInputSsn4InformationInput,
)
from ..models.list_all_envelope_recipients_id_check_information_input_ssn_9_information_input import (
    ListAllEnvelopeRecipientsIdCheckInformationInputSsn9InformationInput,
)


class ListAllEnvelopeRecipientsIdCheckInformationInput(BaseModel):
    """
    Attributes:
        address_information_input (Optional[ListAllEnvelopeRecipientsIdCheckInformationInputAddressInformationInput]):
        dob_information_input (Optional[ListAllEnvelopeRecipientsIdCheckInformationInputDobInformationInput]):
        ssn_4_information_input (Optional[ListAllEnvelopeRecipientsIdCheckInformationInputSsn4InformationInput]):
        ssn_9_information_input (Optional[ListAllEnvelopeRecipientsIdCheckInformationInputSsn9InformationInput]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address_information_input: Optional[
        "ListAllEnvelopeRecipientsIdCheckInformationInputAddressInformationInput"
    ] = Field(alias="addressInformationInput", default=None)
    dob_information_input: Optional[
        "ListAllEnvelopeRecipientsIdCheckInformationInputDobInformationInput"
    ] = Field(alias="dobInformationInput", default=None)
    ssn_4_information_input: Optional[
        "ListAllEnvelopeRecipientsIdCheckInformationInputSsn4InformationInput"
    ] = Field(alias="ssn4InformationInput", default=None)
    ssn_9_information_input: Optional[
        "ListAllEnvelopeRecipientsIdCheckInformationInputSsn9InformationInput"
    ] = Field(alias="ssn9InformationInput", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsIdCheckInformationInput"],
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
