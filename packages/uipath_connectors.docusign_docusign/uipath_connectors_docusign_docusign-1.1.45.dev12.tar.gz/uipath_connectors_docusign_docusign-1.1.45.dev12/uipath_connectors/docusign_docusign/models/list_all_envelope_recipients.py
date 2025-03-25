from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_access_code_metadata import (
    ListAllEnvelopeRecipientsAccessCodeMetadata,
)
from ..models.list_all_envelope_recipients_additional_notifications_array_item_ref import (
    ListAllEnvelopeRecipientsAdditionalNotificationsArrayItemRef,
)
from ..models.list_all_envelope_recipients_delivery_method_metadata import (
    ListAllEnvelopeRecipientsDeliveryMethodMetadata,
)
from ..models.list_all_envelope_recipients_document_visibility_array_item_ref import (
    ListAllEnvelopeRecipientsDocumentVisibilityArrayItemRef,
)
from ..models.list_all_envelope_recipients_email_metadata import (
    ListAllEnvelopeRecipientsEmailMetadata,
)
from ..models.list_all_envelope_recipients_email_notification import (
    ListAllEnvelopeRecipientsEmailNotification,
)
from ..models.list_all_envelope_recipients_fax_number_metadata import (
    ListAllEnvelopeRecipientsFaxNumberMetadata,
)
from ..models.list_all_envelope_recipients_first_name_metadata import (
    ListAllEnvelopeRecipientsFirstNameMetadata,
)
from ..models.list_all_envelope_recipients_full_name_metadata import (
    ListAllEnvelopeRecipientsFullNameMetadata,
)
from ..models.list_all_envelope_recipients_id_check_configuration_name_metadata import (
    ListAllEnvelopeRecipientsIdCheckConfigurationNameMetadata,
)
from ..models.list_all_envelope_recipients_id_check_information_input import (
    ListAllEnvelopeRecipientsIdCheckInformationInput,
)
from ..models.list_all_envelope_recipients_identity_verification import (
    ListAllEnvelopeRecipientsIdentityVerification,
)
from ..models.list_all_envelope_recipients_is_bulk_recipient_metadata import (
    ListAllEnvelopeRecipientsIsBulkRecipientMetadata,
)
from ..models.list_all_envelope_recipients_last_name_metadata import (
    ListAllEnvelopeRecipientsLastNameMetadata,
)
from ..models.list_all_envelope_recipients_name_metadata import (
    ListAllEnvelopeRecipientsNameMetadata,
)
from ..models.list_all_envelope_recipients_note_metadata import (
    ListAllEnvelopeRecipientsNoteMetadata,
)
from ..models.list_all_envelope_recipients_phone_authentication import (
    ListAllEnvelopeRecipientsPhoneAuthentication,
)
from ..models.list_all_envelope_recipients_phone_number import (
    ListAllEnvelopeRecipientsPhoneNumber,
)
from ..models.list_all_envelope_recipients_proof_file import (
    ListAllEnvelopeRecipientsProofFile,
)
from ..models.list_all_envelope_recipients_recipient_attachments_array_item_ref import (
    ListAllEnvelopeRecipientsRecipientAttachmentsArrayItemRef,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatus,
)
from ..models.list_all_envelope_recipients_recipient_feature_metadata_array_item_ref import (
    ListAllEnvelopeRecipientsRecipientFeatureMetadataArrayItemRef,
)
from ..models.list_all_envelope_recipients_recipient_signature_providers_array_item_ref import (
    ListAllEnvelopeRecipientsRecipientSignatureProvidersArrayItemRef,
)
from ..models.list_all_envelope_recipients_recipient_type_metadata import (
    ListAllEnvelopeRecipientsRecipientTypeMetadata,
)
from ..models.list_all_envelope_recipients_require_id_lookup_metadata import (
    ListAllEnvelopeRecipientsRequireIdLookupMetadata,
)
from ..models.list_all_envelope_recipients_routing_order_metadata import (
    ListAllEnvelopeRecipientsRoutingOrderMetadata,
)
from ..models.list_all_envelope_recipients_sign_in_each_location_metadata import (
    ListAllEnvelopeRecipientsSignInEachLocationMetadata,
)
from ..models.list_all_envelope_recipients_signature_info import (
    ListAllEnvelopeRecipientsSignatureInfo,
)
from ..models.list_all_envelope_recipients_signing_group_id_metadata import (
    ListAllEnvelopeRecipientsSigningGroupIdMetadata,
)
from ..models.list_all_envelope_recipients_signing_group_users_array_item_ref import (
    ListAllEnvelopeRecipientsSigningGroupUsersArrayItemRef,
)
from ..models.list_all_envelope_recipients_sms_authentication import (
    ListAllEnvelopeRecipientsSmsAuthentication,
)
from ..models.list_all_envelope_recipients_social_authentications_array_item_ref import (
    ListAllEnvelopeRecipientsSocialAuthenticationsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs import ListAllEnvelopeRecipientsTabs


class ListAllEnvelopeRecipients(BaseModel):
    """
    Attributes:
        access_code (Optional[str]):  Example: string.
        access_code_metadata (Optional[ListAllEnvelopeRecipientsAccessCodeMetadata]):
        add_access_code_to_email (Optional[str]):  Example: string.
        additional_notifications (Optional[list['ListAllEnvelopeRecipientsAdditionalNotificationsArrayItemRef']]):
        agent_can_edit_email (Optional[str]):  Example: string.
        agent_can_edit_name (Optional[str]):  Example: string.
        allow_system_override_for_locked_recipient (Optional[str]):  Example: string.
        auto_navigation (Optional[str]):  Example: string.
        auto_responded_reason (Optional[str]):  Example: string.
        bulk_recipients_uri (Optional[str]):  Example: string.
        can_sign_offline (Optional[str]):  Example: string.
        client_user_id (Optional[str]):  Example: string.
        completed_count (Optional[str]):  Example: string.
        creation_reason (Optional[str]):  Example: string.
        custom_fields (Optional[list[str]]):
        declined_date_time (Optional[str]):  Example: string.
        declined_reason (Optional[str]):  Example: string.
        default_recipient (Optional[str]):  Example: string.
        delivered_date_time (Optional[str]):  Example: string.
        delivery_method (Optional[str]):  Example: string.
        delivery_method_metadata (Optional[ListAllEnvelopeRecipientsDeliveryMethodMetadata]):
        designator_id (Optional[str]):  Example: string.
        designator_id_guid (Optional[str]):  Example: string.
        document_visibility (Optional[list['ListAllEnvelopeRecipientsDocumentVisibilityArrayItemRef']]):
        email (Optional[str]):  Example: string.
        email_metadata (Optional[ListAllEnvelopeRecipientsEmailMetadata]):
        email_notification (Optional[ListAllEnvelopeRecipientsEmailNotification]):
        embedded_recipient_start_url (Optional[str]):  Example: string.
        excluded_documents (Optional[list[str]]):
        fax_number (Optional[str]):  Example: string.
        fax_number_metadata (Optional[ListAllEnvelopeRecipientsFaxNumberMetadata]):
        first_name (Optional[str]):  Example: string.
        first_name_metadata (Optional[ListAllEnvelopeRecipientsFirstNameMetadata]):
        full_name (Optional[str]):  Example: string.
        full_name_metadata (Optional[ListAllEnvelopeRecipientsFullNameMetadata]):
        id_check_configuration_name (Optional[str]):  Example: string.
        id_check_configuration_name_metadata (Optional[ListAllEnvelopeRecipientsIdCheckConfigurationNameMetadata]):
        id_check_information_input (Optional[ListAllEnvelopeRecipientsIdCheckInformationInput]):
        identity_verification (Optional[ListAllEnvelopeRecipientsIdentityVerification]):
        inherit_email_notification_configuration (Optional[str]):  Example: string.
        is_bulk_recipient (Optional[str]):  Example: string.
        is_bulk_recipient_metadata (Optional[ListAllEnvelopeRecipientsIsBulkRecipientMetadata]):
        last_name (Optional[str]):  Example: string.
        last_name_metadata (Optional[ListAllEnvelopeRecipientsLastNameMetadata]):
        locked_recipient_phone_auth_editable (Optional[str]):  Example: string.
        locked_recipient_sms_editable (Optional[str]):  Example: string.
        name (Optional[str]):  Example: string.
        name_metadata (Optional[ListAllEnvelopeRecipientsNameMetadata]):
        notary_id (Optional[str]):  Example: string.
        note (Optional[str]):  Example: string.
        note_metadata (Optional[ListAllEnvelopeRecipientsNoteMetadata]):
        phone_authentication (Optional[ListAllEnvelopeRecipientsPhoneAuthentication]):
        phone_number (Optional[ListAllEnvelopeRecipientsPhoneNumber]):
        proof_file (Optional[ListAllEnvelopeRecipientsProofFile]):
        recipient_attachments (Optional[list['ListAllEnvelopeRecipientsRecipientAttachmentsArrayItemRef']]):
        recipient_authentication_status (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatus]):
        recipient_feature_metadata (Optional[list['ListAllEnvelopeRecipientsRecipientFeatureMetadataArrayItemRef']]):
        recipient_id (Optional[str]):  Example: string.
        recipient_id_guid (Optional[str]):  Example: string.
        recipient_signature_providers
                (Optional[list['ListAllEnvelopeRecipientsRecipientSignatureProvidersArrayItemRef']]):
        recipient_supplies_tabs (Optional[str]):  Example: string.
        recipient_type (Optional[str]):  Example: string.
        recipient_type_metadata (Optional[ListAllEnvelopeRecipientsRecipientTypeMetadata]):
        require_id_lookup (Optional[str]):  Example: string.
        require_id_lookup_metadata (Optional[ListAllEnvelopeRecipientsRequireIdLookupMetadata]):
        require_sign_on_paper (Optional[str]):  Example: string.
        require_signer_certificate (Optional[str]):  Example: string.
        require_upload_signature (Optional[str]):  Example: string.
        role_name (Optional[str]):  Example: string.
        routing_order (Optional[str]):  Example: string.
        routing_order_metadata (Optional[ListAllEnvelopeRecipientsRoutingOrderMetadata]):
        sent_date_time (Optional[str]):  Example: string.
        sign_in_each_location (Optional[str]):  Example: string.
        sign_in_each_location_metadata (Optional[ListAllEnvelopeRecipientsSignInEachLocationMetadata]):
        signature_info (Optional[ListAllEnvelopeRecipientsSignatureInfo]):
        signed_date_time (Optional[str]):  Example: string.
        signing_group_id (Optional[str]):  Example: string.
        signing_group_id_metadata (Optional[ListAllEnvelopeRecipientsSigningGroupIdMetadata]):
        signing_group_name (Optional[str]):  Example: string.
        signing_group_users (Optional[list['ListAllEnvelopeRecipientsSigningGroupUsersArrayItemRef']]):
        sms_authentication (Optional[ListAllEnvelopeRecipientsSmsAuthentication]):
        social_authentications (Optional[list['ListAllEnvelopeRecipientsSocialAuthenticationsArrayItemRef']]):
        status (Optional[str]):  Example: string.
        status_code (Optional[str]):  Example: string.
        suppress_emails (Optional[str]):  Example: string.
        tabs (Optional[ListAllEnvelopeRecipientsTabs]):
        template_locked (Optional[str]):  Example: string.
        template_required (Optional[str]):  Example: string.
        total_tab_count (Optional[str]):  Example: string.
        user_id (Optional[str]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access_code: Optional[str] = Field(alias="accessCode", default=None)
    access_code_metadata: Optional["ListAllEnvelopeRecipientsAccessCodeMetadata"] = (
        Field(alias="accessCodeMetadata", default=None)
    )
    add_access_code_to_email: Optional[str] = Field(
        alias="addAccessCodeToEmail", default=None
    )
    additional_notifications: Optional[
        list["ListAllEnvelopeRecipientsAdditionalNotificationsArrayItemRef"]
    ] = Field(alias="additionalNotifications", default=None)
    agent_can_edit_email: Optional[str] = Field(alias="agentCanEditEmail", default=None)
    agent_can_edit_name: Optional[str] = Field(alias="agentCanEditName", default=None)
    allow_system_override_for_locked_recipient: Optional[str] = Field(
        alias="allowSystemOverrideForLockedRecipient", default=None
    )
    auto_navigation: Optional[str] = Field(alias="autoNavigation", default=None)
    auto_responded_reason: Optional[str] = Field(
        alias="autoRespondedReason", default=None
    )
    bulk_recipients_uri: Optional[str] = Field(alias="bulkRecipientsUri", default=None)
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
    delivery_method_metadata: Optional[
        "ListAllEnvelopeRecipientsDeliveryMethodMetadata"
    ] = Field(alias="deliveryMethodMetadata", default=None)
    designator_id: Optional[str] = Field(alias="designatorId", default=None)
    designator_id_guid: Optional[str] = Field(alias="designatorIdGuid", default=None)
    document_visibility: Optional[
        list["ListAllEnvelopeRecipientsDocumentVisibilityArrayItemRef"]
    ] = Field(alias="documentVisibility", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    email_metadata: Optional["ListAllEnvelopeRecipientsEmailMetadata"] = Field(
        alias="emailMetadata", default=None
    )
    email_notification: Optional["ListAllEnvelopeRecipientsEmailNotification"] = Field(
        alias="emailNotification", default=None
    )
    embedded_recipient_start_url: Optional[str] = Field(
        alias="embeddedRecipientStartURL", default=None
    )
    excluded_documents: Optional[list[str]] = Field(
        alias="excludedDocuments", default=None
    )
    fax_number: Optional[str] = Field(alias="faxNumber", default=None)
    fax_number_metadata: Optional["ListAllEnvelopeRecipientsFaxNumberMetadata"] = Field(
        alias="faxNumberMetadata", default=None
    )
    first_name: Optional[str] = Field(alias="firstName", default=None)
    first_name_metadata: Optional["ListAllEnvelopeRecipientsFirstNameMetadata"] = Field(
        alias="firstNameMetadata", default=None
    )
    full_name: Optional[str] = Field(alias="fullName", default=None)
    full_name_metadata: Optional["ListAllEnvelopeRecipientsFullNameMetadata"] = Field(
        alias="fullNameMetadata", default=None
    )
    id_check_configuration_name: Optional[str] = Field(
        alias="idCheckConfigurationName", default=None
    )
    id_check_configuration_name_metadata: Optional[
        "ListAllEnvelopeRecipientsIdCheckConfigurationNameMetadata"
    ] = Field(alias="idCheckConfigurationNameMetadata", default=None)
    id_check_information_input: Optional[
        "ListAllEnvelopeRecipientsIdCheckInformationInput"
    ] = Field(alias="idCheckInformationInput", default=None)
    identity_verification: Optional["ListAllEnvelopeRecipientsIdentityVerification"] = (
        Field(alias="identityVerification", default=None)
    )
    inherit_email_notification_configuration: Optional[str] = Field(
        alias="inheritEmailNotificationConfiguration", default=None
    )
    is_bulk_recipient: Optional[str] = Field(alias="isBulkRecipient", default=None)
    is_bulk_recipient_metadata: Optional[
        "ListAllEnvelopeRecipientsIsBulkRecipientMetadata"
    ] = Field(alias="isBulkRecipientMetadata", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    last_name_metadata: Optional["ListAllEnvelopeRecipientsLastNameMetadata"] = Field(
        alias="lastNameMetadata", default=None
    )
    locked_recipient_phone_auth_editable: Optional[str] = Field(
        alias="lockedRecipientPhoneAuthEditable", default=None
    )
    locked_recipient_sms_editable: Optional[str] = Field(
        alias="lockedRecipientSmsEditable", default=None
    )
    name: Optional[str] = Field(alias="name", default=None)
    name_metadata: Optional["ListAllEnvelopeRecipientsNameMetadata"] = Field(
        alias="nameMetadata", default=None
    )
    notary_id: Optional[str] = Field(alias="notaryId", default=None)
    note: Optional[str] = Field(alias="note", default=None)
    note_metadata: Optional["ListAllEnvelopeRecipientsNoteMetadata"] = Field(
        alias="noteMetadata", default=None
    )
    phone_authentication: Optional["ListAllEnvelopeRecipientsPhoneAuthentication"] = (
        Field(alias="phoneAuthentication", default=None)
    )
    phone_number: Optional["ListAllEnvelopeRecipientsPhoneNumber"] = Field(
        alias="phoneNumber", default=None
    )
    proof_file: Optional["ListAllEnvelopeRecipientsProofFile"] = Field(
        alias="proofFile", default=None
    )
    recipient_attachments: Optional[
        list["ListAllEnvelopeRecipientsRecipientAttachmentsArrayItemRef"]
    ] = Field(alias="recipientAttachments", default=None)
    recipient_authentication_status: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatus"
    ] = Field(alias="recipientAuthenticationStatus", default=None)
    recipient_feature_metadata: Optional[
        list["ListAllEnvelopeRecipientsRecipientFeatureMetadataArrayItemRef"]
    ] = Field(alias="recipientFeatureMetadata", default=None)
    recipient_id: Optional[str] = Field(alias="recipientId", default=None)
    recipient_id_guid: Optional[str] = Field(alias="recipientIdGuid", default=None)
    recipient_signature_providers: Optional[
        list["ListAllEnvelopeRecipientsRecipientSignatureProvidersArrayItemRef"]
    ] = Field(alias="recipientSignatureProviders", default=None)
    recipient_supplies_tabs: Optional[str] = Field(
        alias="recipientSuppliesTabs", default=None
    )
    recipient_type: Optional[str] = Field(alias="recipientType", default=None)
    recipient_type_metadata: Optional[
        "ListAllEnvelopeRecipientsRecipientTypeMetadata"
    ] = Field(alias="recipientTypeMetadata", default=None)
    require_id_lookup: Optional[str] = Field(alias="requireIdLookup", default=None)
    require_id_lookup_metadata: Optional[
        "ListAllEnvelopeRecipientsRequireIdLookupMetadata"
    ] = Field(alias="requireIdLookupMetadata", default=None)
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
    routing_order_metadata: Optional[
        "ListAllEnvelopeRecipientsRoutingOrderMetadata"
    ] = Field(alias="routingOrderMetadata", default=None)
    sent_date_time: Optional[str] = Field(alias="sentDateTime", default=None)
    sign_in_each_location: Optional[str] = Field(
        alias="signInEachLocation", default=None
    )
    sign_in_each_location_metadata: Optional[
        "ListAllEnvelopeRecipientsSignInEachLocationMetadata"
    ] = Field(alias="signInEachLocationMetadata", default=None)
    signature_info: Optional["ListAllEnvelopeRecipientsSignatureInfo"] = Field(
        alias="signatureInfo", default=None
    )
    signed_date_time: Optional[str] = Field(alias="signedDateTime", default=None)
    signing_group_id: Optional[str] = Field(alias="signingGroupId", default=None)
    signing_group_id_metadata: Optional[
        "ListAllEnvelopeRecipientsSigningGroupIdMetadata"
    ] = Field(alias="signingGroupIdMetadata", default=None)
    signing_group_name: Optional[str] = Field(alias="signingGroupName", default=None)
    signing_group_users: Optional[
        list["ListAllEnvelopeRecipientsSigningGroupUsersArrayItemRef"]
    ] = Field(alias="signingGroupUsers", default=None)
    sms_authentication: Optional["ListAllEnvelopeRecipientsSmsAuthentication"] = Field(
        alias="smsAuthentication", default=None
    )
    social_authentications: Optional[
        list["ListAllEnvelopeRecipientsSocialAuthenticationsArrayItemRef"]
    ] = Field(alias="socialAuthentications", default=None)
    status: Optional[str] = Field(alias="status", default=None)
    status_code: Optional[str] = Field(alias="statusCode", default=None)
    suppress_emails: Optional[str] = Field(alias="suppressEmails", default=None)
    tabs: Optional["ListAllEnvelopeRecipientsTabs"] = Field(alias="tabs", default=None)
    template_locked: Optional[str] = Field(alias="templateLocked", default=None)
    template_required: Optional[str] = Field(alias="templateRequired", default=None)
    total_tab_count: Optional[str] = Field(alias="totalTabCount", default=None)
    user_id: Optional[str] = Field(alias="userId", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListAllEnvelopeRecipients"], src_dict: Dict[str, Any]):
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
