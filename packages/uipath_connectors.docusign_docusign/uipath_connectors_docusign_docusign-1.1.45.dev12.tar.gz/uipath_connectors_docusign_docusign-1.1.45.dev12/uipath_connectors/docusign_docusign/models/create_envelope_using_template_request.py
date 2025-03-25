from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_envelope_using_template_request_status import (
    CreateEnvelopeUsingTemplateRequestStatus,
)


class CreateEnvelopeUsingTemplateRequest(BaseModel):
    """
    Attributes:
        status (CreateEnvelopeUsingTemplateRequestStatus): Indicates the envelope status. Valid values when creating an
                envelope are “draft” for creating a draft envelope or “send” for creating and sending the envelope to
                recipients. Example: Send.
        template_id (str): Type the name or ID of the template. If the template is not found in the drop-down, you can
                first scroll the drop-down till the bottom to get all the available templates and then type the template or
                retrieve the template ID from "List All Records->Templates" Example: 1d8136d6-05f7-4617-ad98-ea538617bb74.
        allow_reassign (Optional[bool]): When true, the recipient can redirect an envelope to a more appropriate
                recipient Example: True.
        email_blurb (Optional[str]): The body of the email message that is sent to all envelope recipients Example:
                docusign email sample.
        email_subject (Optional[str]): The subject line of the email message to be sent to all recipients. Required when
                “send” is selected as status, while creating the envelope. Example: dousing REST API Quickstart Sample.
        recipient_email (Optional[str]): The email address of the recipient. The system sends notifications about the
                documents to sign to this address. Required when “send” is selected as status, while creating the envelope.
                Example: amit.espsofttech@gmail.com.
        recipient_name (Optional[str]): The full legal name of the recipient. Required when “send” is selected as status
                while creating the envelope. Example: Amit Tiwari.
        recipient_role (Optional[str]): The user defined role for the recipient. For example, “Applicant 1”, “Applicant
                2”, “Signer”, “Agent”, “Editor” etc. Defaulted to  “Signer”  Example: testroleName.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    status: "CreateEnvelopeUsingTemplateRequestStatus" = Field(alias="status")
    template_id: str = Field(alias="templateId")
    allow_reassign: Optional[bool] = Field(alias="allowReassign", default=None)
    email_blurb: Optional[str] = Field(alias="emailBlurb", default=None)
    email_subject: Optional[str] = Field(alias="emailSubject", default=None)
    recipient_email: Optional[str] = Field(alias="recipientEmail", default=None)
    recipient_name: Optional[str] = Field(alias="recipientName", default=None)
    recipient_role: Optional[str] = Field(alias="recipientRole", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateEnvelopeUsingTemplateRequest"], src_dict: Dict[str, Any]
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
