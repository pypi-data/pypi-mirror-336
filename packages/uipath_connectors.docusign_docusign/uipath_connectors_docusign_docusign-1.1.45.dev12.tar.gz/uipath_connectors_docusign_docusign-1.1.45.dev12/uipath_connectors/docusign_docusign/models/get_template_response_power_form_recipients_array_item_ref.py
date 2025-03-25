from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetTemplateResponsePowerFormRecipientsArrayItemRef(BaseModel):
    """
    Attributes:
        access_code (Optional[str]):
        access_code_locked (Optional[str]):
        access_code_required (Optional[str]):
        email (Optional[str]):
        email_locked (Optional[str]):
        id_check_configuration_name (Optional[str]):
        id_check_required (Optional[str]):
        name (Optional[str]):
        recipient_type (Optional[str]):
        role_name (Optional[str]):
        routing_order (Optional[str]):
        template_requires_id_lookup (Optional[str]):
        user_name_locked (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access_code: Optional[str] = Field(alias="accessCode", default=None)
    access_code_locked: Optional[str] = Field(alias="accessCodeLocked", default=None)
    access_code_required: Optional[str] = Field(
        alias="accessCodeRequired", default=None
    )
    email: Optional[str] = Field(alias="email", default=None)
    email_locked: Optional[str] = Field(alias="emailLocked", default=None)
    id_check_configuration_name: Optional[str] = Field(
        alias="idCheckConfigurationName", default=None
    )
    id_check_required: Optional[str] = Field(alias="idCheckRequired", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    recipient_type: Optional[str] = Field(alias="recipientType", default=None)
    role_name: Optional[str] = Field(alias="roleName", default=None)
    routing_order: Optional[str] = Field(alias="routingOrder", default=None)
    template_requires_id_lookup: Optional[str] = Field(
        alias="templateRequiresIdLookup", default=None
    )
    user_name_locked: Optional[str] = Field(alias="userNameLocked", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetTemplateResponsePowerFormRecipientsArrayItemRef"],
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
