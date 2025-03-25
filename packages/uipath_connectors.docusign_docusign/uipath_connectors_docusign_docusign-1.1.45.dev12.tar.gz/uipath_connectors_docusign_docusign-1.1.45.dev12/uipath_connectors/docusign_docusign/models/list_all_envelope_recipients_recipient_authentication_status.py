from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_recipient_authentication_status_access_code_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusAccessCodeResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_age_verify_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusAgeVerifyResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_any_social_id_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusAnySocialIDResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_facebook_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusFacebookResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_google_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusGoogleResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_id_lookup_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdLookupResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_id_questions_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdQuestionsResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_identity_verification_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdentityVerificationResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_linkedin_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusLinkedinResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_live_id_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusLiveIDResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_ofac_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusOfacResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_open_id_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusOpenIDResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_phone_auth_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusPhoneAuthResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_salesforce_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusSalesforceResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_signature_provider_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusSignatureProviderResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_sms_auth_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusSmsAuthResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_stan_pin_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusSTANPinResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_twitter_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusTwitterResult,
)
from ..models.list_all_envelope_recipients_recipient_authentication_status_yahoo_result import (
    ListAllEnvelopeRecipientsRecipientAuthenticationStatusYahooResult,
)


class ListAllEnvelopeRecipientsRecipientAuthenticationStatus(BaseModel):
    """
    Attributes:
        access_code_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusAccessCodeResult]):
        age_verify_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusAgeVerifyResult]):
        any_social_id_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusAnySocialIDResult]):
        facebook_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusFacebookResult]):
        google_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusGoogleResult]):
        id_lookup_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdLookupResult]):
        id_questions_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdQuestionsResult]):
        identity_verification_result
                (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdentityVerificationResult]):
        linkedin_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusLinkedinResult]):
        live_id_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusLiveIDResult]):
        ofac_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusOfacResult]):
        open_id_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusOpenIDResult]):
        phone_auth_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusPhoneAuthResult]):
        s_tan_pin_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusSTANPinResult]):
        salesforce_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusSalesforceResult]):
        signature_provider_result
                (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusSignatureProviderResult]):
        sms_auth_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusSmsAuthResult]):
        twitter_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusTwitterResult]):
        yahoo_result (Optional[ListAllEnvelopeRecipientsRecipientAuthenticationStatusYahooResult]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access_code_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusAccessCodeResult"
    ] = Field(alias="accessCodeResult", default=None)
    age_verify_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusAgeVerifyResult"
    ] = Field(alias="ageVerifyResult", default=None)
    any_social_id_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusAnySocialIDResult"
    ] = Field(alias="anySocialIDResult", default=None)
    facebook_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusFacebookResult"
    ] = Field(alias="facebookResult", default=None)
    google_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusGoogleResult"
    ] = Field(alias="googleResult", default=None)
    id_lookup_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdLookupResult"
    ] = Field(alias="idLookupResult", default=None)
    id_questions_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdQuestionsResult"
    ] = Field(alias="idQuestionsResult", default=None)
    identity_verification_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusIdentityVerificationResult"
    ] = Field(alias="identityVerificationResult", default=None)
    linkedin_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusLinkedinResult"
    ] = Field(alias="linkedinResult", default=None)
    live_id_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusLiveIDResult"
    ] = Field(alias="liveIDResult", default=None)
    ofac_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusOfacResult"
    ] = Field(alias="ofacResult", default=None)
    open_id_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusOpenIDResult"
    ] = Field(alias="openIDResult", default=None)
    phone_auth_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusPhoneAuthResult"
    ] = Field(alias="phoneAuthResult", default=None)
    s_tan_pin_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusSTANPinResult"
    ] = Field(alias="sTANPinResult", default=None)
    salesforce_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusSalesforceResult"
    ] = Field(alias="salesforceResult", default=None)
    signature_provider_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusSignatureProviderResult"
    ] = Field(alias="signatureProviderResult", default=None)
    sms_auth_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusSmsAuthResult"
    ] = Field(alias="smsAuthResult", default=None)
    twitter_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusTwitterResult"
    ] = Field(alias="twitterResult", default=None)
    yahoo_result: Optional[
        "ListAllEnvelopeRecipientsRecipientAuthenticationStatusYahooResult"
    ] = Field(alias="yahooResult", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["ListAllEnvelopeRecipientsRecipientAuthenticationStatus"],
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
