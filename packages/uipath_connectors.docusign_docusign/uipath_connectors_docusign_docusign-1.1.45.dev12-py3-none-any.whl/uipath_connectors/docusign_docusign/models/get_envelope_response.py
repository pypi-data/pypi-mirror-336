from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_envelope_response_email_settings import (
    GetEnvelopeResponseEmailSettings,
)
from ..models.get_envelope_response_envelope_attachments_array_item_ref import (
    GetEnvelopeResponseEnvelopeAttachmentsArrayItemRef,
)
from ..models.get_envelope_response_envelope_documents_array_item_ref import (
    GetEnvelopeResponseEnvelopeDocumentsArrayItemRef,
)
from ..models.get_envelope_response_envelope_metadata import (
    GetEnvelopeResponseEnvelopeMetadata,
)
from ..models.get_envelope_response_folders_array_item_ref import (
    GetEnvelopeResponseFoldersArrayItemRef,
)
from ..models.get_envelope_response_notification import GetEnvelopeResponseNotification
from ..models.get_envelope_response_power_form import GetEnvelopeResponsePowerForm
from ..models.get_envelope_response_status import GetEnvelopeResponseStatus
from ..models.get_envelope_response_workflow import GetEnvelopeResponseWorkflow
import datetime


class GetEnvelopeResponse(BaseModel):
    """
    Attributes:
        access_control_list_base_64 (Optional[str]):
        allow_comments (Optional[str]):
        allow_markup (Optional[str]):
        allow_reassign (Optional[str]):
        allow_view_history (Optional[str]):
        any_signer (Optional[str]):
        asynchronous (Optional[str]):
        attachments_uri (Optional[str]):
        authoritative_copy (Optional[str]):
        authoritative_copy_default (Optional[str]):
        auto_navigation (Optional[str]):
        brand_id (Optional[str]):
        brand_lock (Optional[str]):
        certificate_uri (Optional[str]):
        completed_date_time (Optional[datetime.datetime]):
        copy_recipient_data (Optional[str]):
        created_date_time (Optional[datetime.datetime]):
        custom_fields_uri (Optional[str]):
        declined_date_time (Optional[datetime.datetime]):
        deleted_date_time (Optional[datetime.datetime]):
        delivered_date_time (Optional[datetime.datetime]):
        disable_responsive_document (Optional[str]):
        document_base_64 (Optional[str]):
        documents_combined_uri (Optional[str]):
        documents_uri (Optional[str]):
        email_blurb (Optional[str]):
        email_settings (Optional[GetEnvelopeResponseEmailSettings]):
        email_subject (Optional[str]):
        enable_wet_sign (Optional[str]):
        enforce_signer_visibility (Optional[str]):
        envelope_attachments (Optional[list['GetEnvelopeResponseEnvelopeAttachmentsArrayItemRef']]):
        envelope_documents (Optional[list['GetEnvelopeResponseEnvelopeDocumentsArrayItemRef']]):
        envelope_id (Optional[str]): Type the name or ID of the envelope. If the envelope is not found in the drop-down,
                you can first scroll the drop-down till the bottom to get all the available envelopes and then type the envelope
                or retrieve the envelope ID from the DocuSign application -> 'Manage' tab -> Goto “Sent” or “Draft” under
                “Envelopes” -> Click on the respective envelope and retrieve the envelope ID from URL. For example, if the URL
                is “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the envelope ID is
                '3ae67e54-f761-4a5b-a23e-b5e4835492cc'
        envelope_id_stamping (Optional[str]):
        envelope_location (Optional[str]):
        envelope_metadata (Optional[GetEnvelopeResponseEnvelopeMetadata]):
        envelope_uri (Optional[str]):
        expire_after (Optional[str]):
        expire_date_time (Optional[datetime.datetime]):
        expire_enabled (Optional[str]):
        external_envelope_id (Optional[str]):
        folders (Optional[list['GetEnvelopeResponseFoldersArrayItemRef']]):
        has_comments (Optional[str]):
        has_form_data_changed (Optional[str]):
        has_wav_file (Optional[str]):
        holder (Optional[str]):
        initial_sent_date_time (Optional[datetime.datetime]):
        is_21cfr_part_11 (Optional[str]):
        is_dynamic_envelope (Optional[str]):
        is_signature_provider_envelope (Optional[str]):
        last_modified_date_time (Optional[datetime.datetime]):
        location (Optional[str]):
        message_lock (Optional[str]):
        notification (Optional[GetEnvelopeResponseNotification]):
        notification_uri (Optional[str]):
        power_form (Optional[GetEnvelopeResponsePowerForm]):
        purge_completed_date (Optional[str]):
        purge_request_date (Optional[str]):
        purge_state (Optional[str]):
        recipients_lock (Optional[str]):
        recipients_uri (Optional[str]):
        sent_date_time (Optional[datetime.datetime]):
        signer_can_sign_on_mobile (Optional[str]):
        signing_location (Optional[str]):
        status (Optional[GetEnvelopeResponseStatus]):
        status_changed_date_time (Optional[datetime.datetime]):
        status_date_time (Optional[datetime.datetime]):
        templates_uri (Optional[str]):
        transaction_id (Optional[str]):
        use_disclosure (Optional[str]):
        voided_date_time (Optional[str]):
        voided_reason (Optional[str]):
        workflow (Optional[GetEnvelopeResponseWorkflow]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access_control_list_base_64: Optional[str] = Field(
        alias="accessControlListBase64", default=None
    )
    allow_comments: Optional[str] = Field(alias="allowComments", default=None)
    allow_markup: Optional[str] = Field(alias="allowMarkup", default=None)
    allow_reassign: Optional[str] = Field(alias="allowReassign", default=None)
    allow_view_history: Optional[str] = Field(alias="allowViewHistory", default=None)
    any_signer: Optional[str] = Field(alias="anySigner", default=None)
    asynchronous: Optional[str] = Field(alias="asynchronous", default=None)
    attachments_uri: Optional[str] = Field(alias="attachmentsUri", default=None)
    authoritative_copy: Optional[str] = Field(alias="authoritativeCopy", default=None)
    authoritative_copy_default: Optional[str] = Field(
        alias="authoritativeCopyDefault", default=None
    )
    auto_navigation: Optional[str] = Field(alias="autoNavigation", default=None)
    brand_id: Optional[str] = Field(alias="brandId", default=None)
    brand_lock: Optional[str] = Field(alias="brandLock", default=None)
    certificate_uri: Optional[str] = Field(alias="certificateUri", default=None)
    completed_date_time: Optional[datetime.datetime] = Field(
        alias="completedDateTime", default=None
    )
    copy_recipient_data: Optional[str] = Field(alias="copyRecipientData", default=None)
    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    custom_fields_uri: Optional[str] = Field(alias="customFieldsUri", default=None)
    declined_date_time: Optional[datetime.datetime] = Field(
        alias="declinedDateTime", default=None
    )
    deleted_date_time: Optional[datetime.datetime] = Field(
        alias="deletedDateTime", default=None
    )
    delivered_date_time: Optional[datetime.datetime] = Field(
        alias="deliveredDateTime", default=None
    )
    disable_responsive_document: Optional[str] = Field(
        alias="disableResponsiveDocument", default=None
    )
    document_base_64: Optional[str] = Field(alias="documentBase64", default=None)
    documents_combined_uri: Optional[str] = Field(
        alias="documentsCombinedUri", default=None
    )
    documents_uri: Optional[str] = Field(alias="documentsUri", default=None)
    email_blurb: Optional[str] = Field(alias="emailBlurb", default=None)
    email_settings: Optional["GetEnvelopeResponseEmailSettings"] = Field(
        alias="emailSettings", default=None
    )
    email_subject: Optional[str] = Field(alias="emailSubject", default=None)
    enable_wet_sign: Optional[str] = Field(alias="enableWetSign", default=None)
    enforce_signer_visibility: Optional[str] = Field(
        alias="enforceSignerVisibility", default=None
    )
    envelope_attachments: Optional[
        list["GetEnvelopeResponseEnvelopeAttachmentsArrayItemRef"]
    ] = Field(alias="envelopeAttachments", default=None)
    envelope_documents: Optional[
        list["GetEnvelopeResponseEnvelopeDocumentsArrayItemRef"]
    ] = Field(alias="envelopeDocuments", default=None)
    envelope_id: Optional[str] = Field(alias="envelopeId", default=None)
    envelope_id_stamping: Optional[str] = Field(
        alias="envelopeIdStamping", default=None
    )
    envelope_location: Optional[str] = Field(alias="envelopeLocation", default=None)
    envelope_metadata: Optional["GetEnvelopeResponseEnvelopeMetadata"] = Field(
        alias="envelopeMetadata", default=None
    )
    envelope_uri: Optional[str] = Field(alias="envelopeUri", default=None)
    expire_after: Optional[str] = Field(alias="expireAfter", default=None)
    expire_date_time: Optional[datetime.datetime] = Field(
        alias="expireDateTime", default=None
    )
    expire_enabled: Optional[str] = Field(alias="expireEnabled", default=None)
    external_envelope_id: Optional[str] = Field(
        alias="externalEnvelopeId", default=None
    )
    folders: Optional[list["GetEnvelopeResponseFoldersArrayItemRef"]] = Field(
        alias="folders", default=None
    )
    has_comments: Optional[str] = Field(alias="hasComments", default=None)
    has_form_data_changed: Optional[str] = Field(
        alias="hasFormDataChanged", default=None
    )
    has_wav_file: Optional[str] = Field(alias="hasWavFile", default=None)
    holder: Optional[str] = Field(alias="holder", default=None)
    initial_sent_date_time: Optional[datetime.datetime] = Field(
        alias="initialSentDateTime", default=None
    )
    is_21cfr_part_11: Optional[str] = Field(alias="is21CFRPart11", default=None)
    is_dynamic_envelope: Optional[str] = Field(alias="isDynamicEnvelope", default=None)
    is_signature_provider_envelope: Optional[str] = Field(
        alias="isSignatureProviderEnvelope", default=None
    )
    last_modified_date_time: Optional[datetime.datetime] = Field(
        alias="lastModifiedDateTime", default=None
    )
    location: Optional[str] = Field(alias="location", default=None)
    message_lock: Optional[str] = Field(alias="messageLock", default=None)
    notification: Optional["GetEnvelopeResponseNotification"] = Field(
        alias="notification", default=None
    )
    notification_uri: Optional[str] = Field(alias="notificationUri", default=None)
    power_form: Optional["GetEnvelopeResponsePowerForm"] = Field(
        alias="powerForm", default=None
    )
    purge_completed_date: Optional[str] = Field(
        alias="purgeCompletedDate", default=None
    )
    purge_request_date: Optional[str] = Field(alias="purgeRequestDate", default=None)
    purge_state: Optional[str] = Field(alias="purgeState", default=None)
    recipients_lock: Optional[str] = Field(alias="recipientsLock", default=None)
    recipients_uri: Optional[str] = Field(alias="recipientsUri", default=None)
    sent_date_time: Optional[datetime.datetime] = Field(
        alias="sentDateTime", default=None
    )
    signer_can_sign_on_mobile: Optional[str] = Field(
        alias="signerCanSignOnMobile", default=None
    )
    signing_location: Optional[str] = Field(alias="signingLocation", default=None)
    status: Optional["GetEnvelopeResponseStatus"] = Field(alias="status", default=None)
    status_changed_date_time: Optional[datetime.datetime] = Field(
        alias="statusChangedDateTime", default=None
    )
    status_date_time: Optional[datetime.datetime] = Field(
        alias="statusDateTime", default=None
    )
    templates_uri: Optional[str] = Field(alias="templatesUri", default=None)
    transaction_id: Optional[str] = Field(alias="transactionId", default=None)
    use_disclosure: Optional[str] = Field(alias="useDisclosure", default=None)
    voided_date_time: Optional[str] = Field(alias="voidedDateTime", default=None)
    voided_reason: Optional[str] = Field(alias="voidedReason", default=None)
    workflow: Optional["GetEnvelopeResponseWorkflow"] = Field(
        alias="workflow", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEnvelopeResponse"], src_dict: Dict[str, Any]):
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
