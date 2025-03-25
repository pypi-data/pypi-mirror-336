from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class CreateByCopyingEnvelopeRequest(BaseModel):
    """
    Attributes:
        clone_envelope_id (str): Type the name or ID of the envelope to clone. If the envelope is not found in the drop-
                down, you can first scroll the drop-down till the bottom to get all the available envelopes and then type the
                envelope or retrieve the envelope ID from the DocuSign application -> "Manage" tab -> Goto "Sent" or "Draft"
                under “Envelopes” -> Click on the respective envelope and retrieve the envelope ID from URL. For example, if the
                URL is “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the envelope ID is
                “3ae67e54-f761-4a5b-a23e-b5e4835492cc”
        copy_recipient_data (Optional[bool]): Whether to include the recipient field values of the existing envelope?
                Default is false. Only values from data entry fields, like checkboxes and radio buttons, will be copied. Fields
                that require an action, like signatures and initials, will not be included. Example: True.
        email_blurb (Optional[str]): The body of the email message that is sent to all the envelope recipients. This
                will overwrite the email body copied from the existing envelope Example: Shows how to create and send an
                envelope from a document..
        email_subject (Optional[str]): The subject line of the email that that will be sent to all recipients. This will
                overwrite the email subject copied from the existing envelope Example: dousing REST API Quickstart Sample.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    clone_envelope_id: str = Field(alias="cloneEnvelopeId")
    copy_recipient_data: Optional[bool] = Field(alias="copyRecipientData", default=None)
    email_blurb: Optional[str] = Field(alias="emailBlurb", default=None)
    email_subject: Optional[str] = Field(alias="emailSubject", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateByCopyingEnvelopeRequest"], src_dict: Dict[str, Any]
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
