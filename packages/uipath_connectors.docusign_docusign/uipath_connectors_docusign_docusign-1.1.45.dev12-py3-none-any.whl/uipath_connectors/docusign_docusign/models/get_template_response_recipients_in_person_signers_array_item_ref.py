from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetTemplateResponseRecipientsInPersonSignersArrayItemRef(BaseModel):
    """
    Attributes:
        access_code (Optional[str]):
        add_access_code_to_email (Optional[str]):
        allow_system_override_for_locked_recipient (Optional[str]):
        auto_navigation (Optional[str]):
        auto_responded_reason (Optional[str]):
        can_sign_offline (Optional[str]):
        client_user_id (Optional[str]):
        completed_count (Optional[str]):
        creation_reason (Optional[str]):
        custom_fields (Optional[list[str]]):
        declined_date_time (Optional[str]):
        declined_reason (Optional[str]):
        default_recipient (Optional[str]):
        delivered_date_time (Optional[str]):
        delivery_method (Optional[str]):
        designator_id (Optional[str]):
        designator_id_guid (Optional[str]):
        email (Optional[str]):
        embedded_recipient_start_url (Optional[str]):
        excluded_documents (Optional[list[str]]):
        fax_number (Optional[str]):
        host_email (Optional[str]):
        host_name (Optional[str]):
        id_check_configuration_name (Optional[str]):
        in_person_signing_type (Optional[str]):
        inherit_email_notification_configuration (Optional[str]):
        locked_recipient_phone_auth_editable (Optional[str]):
        locked_recipient_sms_editable (Optional[str]):
        name (Optional[str]):
        notary_id (Optional[str]):
        note (Optional[str]):
        recipient_id (Optional[str]):
        recipient_id_guid (Optional[str]):
        recipient_supplies_tabs (Optional[str]):
        recipient_type (Optional[str]):
        require_id_lookup (Optional[str]):
        require_sign_on_paper (Optional[str]):
        require_signer_certificate (Optional[str]):
        require_upload_signature (Optional[str]):
        role_name (Optional[str]):
        routing_order (Optional[str]):
        sent_date_time (Optional[str]):
        sign_in_each_location (Optional[str]):
        signed_date_time (Optional[str]):
        signer_email (Optional[str]):
        signer_first_name (Optional[str]):
        signer_last_name (Optional[str]):
        signer_name (Optional[str]):
        signing_group_id (Optional[str]):
        signing_group_name (Optional[str]):
        status (Optional[str]):
        status_code (Optional[str]):
        suppress_emails (Optional[str]):
        template_locked (Optional[str]):
        template_required (Optional[str]):
        total_tab_count (Optional[str]):
        user_id (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access_code: Optional[str] = Field(alias="accessCode", default=None)
    add_access_code_to_email: Optional[str] = Field(
        alias="addAccessCodeToEmail", default=None
    )
    allow_system_override_for_locked_recipient: Optional[str] = Field(
        alias="allowSystemOverrideForLockedRecipient", default=None
    )
    auto_navigation: Optional[str] = Field(alias="autoNavigation", default=None)
    auto_responded_reason: Optional[str] = Field(
        alias="autoRespondedReason", default=None
    )
    can_sign_offline: Optional[str] = Field(alias="canSignOffline", default=None)
    client_user_id: Optional[str] = Field(alias="clientUserId", default=None)
    completed_count: Optional[str] = Field(alias="completedCount", default=None)
    creation_reason: Optional[str] = Field(alias="creationReason", default=None)
    custom_fields: Optional[list[str]] = Field(alias="customFields", default=None)
    declined_date_time: Optional[str] = Field(alias="declinedDateTime", default=None)
    declined_reason: Optional[str] = Field(alias="declinedReason", default=None)
    default_recipient: Optional[str] = Field(alias="defaultRecipient", default=None)
    delivered_date_time: Optional[str] = Field(alias="deliveredDateTime", default=None)
    delivery_method: Optional[str] = Field(alias="deliveryMethod", default=None)
    designator_id: Optional[str] = Field(alias="designatorId", default=None)
    designator_id_guid: Optional[str] = Field(alias="designatorIdGuid", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    embedded_recipient_start_url: Optional[str] = Field(
        alias="embeddedRecipientStartURL", default=None
    )
    excluded_documents: Optional[list[str]] = Field(
        alias="excludedDocuments", default=None
    )
    fax_number: Optional[str] = Field(alias="faxNumber", default=None)
    host_email: Optional[str] = Field(alias="hostEmail", default=None)
    host_name: Optional[str] = Field(alias="hostName", default=None)
    id_check_configuration_name: Optional[str] = Field(
        alias="idCheckConfigurationName", default=None
    )
    in_person_signing_type: Optional[str] = Field(
        alias="inPersonSigningType", default=None
    )
    inherit_email_notification_configuration: Optional[str] = Field(
        alias="inheritEmailNotificationConfiguration", default=None
    )
    locked_recipient_phone_auth_editable: Optional[str] = Field(
        alias="lockedRecipientPhoneAuthEditable", default=None
    )
    locked_recipient_sms_editable: Optional[str] = Field(
        alias="lockedRecipientSmsEditable", default=None
    )
    name: Optional[str] = Field(alias="name", default=None)
    notary_id: Optional[str] = Field(alias="notaryId", default=None)
    note: Optional[str] = Field(alias="note", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_supplies_tabs: Optional[str] = Field(
        alias="recipientSuppliesTabs", default=None
    )
    recipient_type: Optional[str] = Field(alias="recipientType", default=None)
    require_id_lookup: Optional[str] = Field(alias="requireIdLookup", default=None)
    require_sign_on_paper: Optional[str] = Field(
        alias="requireSignOnPaper", default=None
    )
    require_signer_certificate: Optional[str] = Field(
        alias="requireSignerCertificate", default=None
    )
    require_upload_signature: Optional[str] = Field(
        alias="requireUploadSignature", default=None
    )
    role_name: Optional[str] = Field(alias="roleName", default=None)
    routing_order: Optional[str] = Field(alias="routingOrder", default=None)
    sent_date_time: Optional[str] = Field(alias="sentDateTime", default=None)
    sign_in_each_location: Optional[str] = Field(
        alias="signInEachLocation", default=None
    )
    signed_date_time: Optional[str] = Field(alias="signedDateTime", default=None)
    signer_email: Optional[str] = Field(alias="signerEmail", default=None)
    signer_first_name: Optional[str] = Field(alias="signerFirstName", default=None)
    signer_last_name: Optional[str] = Field(alias="signerLastName", default=None)
    signer_name: Optional[str] = Field(alias="signerName", default=None)
    signing_group_id: Optional[str] = Field(alias="signingGroupId", default=None)
    signing_group_name: Optional[str] = Field(alias="signingGroupName", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_code: Optional[str] = Field(alias="statusCode", default=None)
    suppress_emails: Optional[str] = Field(alias="suppressEmails", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    total_tab_count: Optional[str] = Field(alias="totalTabCount", default=None)
    user_id: Optional[str] = Field(alias="userId", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetTemplateResponseRecipientsInPersonSignersArrayItemRef"],
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
