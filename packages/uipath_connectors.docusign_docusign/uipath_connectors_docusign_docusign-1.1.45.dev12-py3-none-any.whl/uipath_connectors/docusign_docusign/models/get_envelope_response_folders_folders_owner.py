from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEnvelopeResponseFoldersFoldersOwner(BaseModel):
    """
    Attributes:
        account_id (Optional[str]):
        account_name (Optional[str]):
        activation_access_code (Optional[str]):
        email (Optional[str]):
        login_status (Optional[str]):
        membership_id (Optional[str]):
        send_activation_email (Optional[str]):
        uri (Optional[str]):
        user_id (Optional[str]):
        user_name (Optional[str]):
        user_status (Optional[str]):
        user_type (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account_id: Optional[str] = Field(alias="accountId", default=None)
    account_name: Optional[str] = Field(alias="accountName", default=None)
    activation_access_code: Optional[str] = Field(
        alias="activationAccessCode", default=None
    )
    email: Optional[str] = Field(alias="email", default=None)
    login_status: Optional[str] = Field(alias="loginStatus", default=None)
    membership_id: Optional[str] = Field(alias="membershipId", default=None)
    send_activation_email: Optional[str] = Field(
        alias="sendActivationEmail", default=None
    )
    uri: Optional[str] = Field(alias="uri", default=None)
    user_id: Optional[str] = Field(alias="userId", default=None)
    user_name: Optional[str] = Field(alias="userName", default=None)
    user_status: Optional[str] = Field(alias="userStatus", default=None)
    user_type: Optional[str] = Field(alias="userType", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEnvelopeResponseFoldersFoldersOwner"], src_dict: Dict[str, Any]
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
