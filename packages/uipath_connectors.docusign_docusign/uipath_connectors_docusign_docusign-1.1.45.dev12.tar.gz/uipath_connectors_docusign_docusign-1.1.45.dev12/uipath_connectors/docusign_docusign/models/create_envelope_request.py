from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Type

from ..models.create_envelope_request_status import CreateEnvelopeRequestStatus


class CreateEnvelopeRequest(BaseModel):
    """
    Attributes:
        email_subject (str): The email subject
        signer_email (str): Email address of the signer
        signer_name (str): Name of the signer
        status (CreateEnvelopeRequestStatus): The status of the envelope. Example: sent.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    email_subject: str = Field(alias="emailSubject")
    signer_email: str = Field(alias="signerEmail")
    signer_name: str = Field(alias="signerName")
    status: "CreateEnvelopeRequestStatus" = Field(alias="status")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateEnvelopeRequest"], src_dict: Dict[str, Any]):
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
