from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_all_envelope_recipients_tabs_approve_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsApproveTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_checkbox_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCheckboxTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_comment_thread_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCommentThreadTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_commission_county_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCommissionCountyTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_commission_expiration_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCommissionExpirationTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_commission_number_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCommissionNumberTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_commission_state_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCommissionStateTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_company_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCompanyTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_currency_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsCurrencyTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_date_signed_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsDateSignedTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_date_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsDateTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_decline_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsDeclineTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_draw_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsDrawTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_email_address_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsEmailAddressTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_email_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsEmailTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_envelope_id_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsEnvelopeIdTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_first_name_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsFirstNameTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_formula_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsFormulaTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_full_name_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsFullNameTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_initial_here_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsInitialHereTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_last_name_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsLastNameTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_list_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsListTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_notarize_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsNotarizeTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_notary_seal_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsNotarySealTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_note_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsNoteTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_number_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsNumberTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_phone_number_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPhoneNumberTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_poly_line_overlay_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_prefill_tabs import (
    ListAllEnvelopeRecipientsTabsPrefillTabs,
)
from ..models.list_all_envelope_recipients_tabs_radio_group_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsRadioGroupTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_sign_here_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsSignHereTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_signer_attachment_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsSignerAttachmentTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_smart_section_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsSmartSectionTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_ssn_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsSsnTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_tab_groups_array_item_ref import (
    ListAllEnvelopeRecipientsTabsTabGroupsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_text_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsTextTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_title_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsTitleTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_view_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsViewTabsArrayItemRef,
)
from ..models.list_all_envelope_recipients_tabs_zip_tabs_array_item_ref import (
    ListAllEnvelopeRecipientsTabsZipTabsArrayItemRef,
)


class ListAllEnvelopeRecipientsTabs(BaseModel):
    """
    Attributes:
        approve_tabs (Optional[list['ListAllEnvelopeRecipientsTabsApproveTabsArrayItemRef']]):
        checkbox_tabs (Optional[list['ListAllEnvelopeRecipientsTabsCheckboxTabsArrayItemRef']]):
        comment_thread_tabs (Optional[list['ListAllEnvelopeRecipientsTabsCommentThreadTabsArrayItemRef']]):
        commission_county_tabs (Optional[list['ListAllEnvelopeRecipientsTabsCommissionCountyTabsArrayItemRef']]):
        commission_expiration_tabs
                (Optional[list['ListAllEnvelopeRecipientsTabsCommissionExpirationTabsArrayItemRef']]):
        commission_number_tabs (Optional[list['ListAllEnvelopeRecipientsTabsCommissionNumberTabsArrayItemRef']]):
        commission_state_tabs (Optional[list['ListAllEnvelopeRecipientsTabsCommissionStateTabsArrayItemRef']]):
        company_tabs (Optional[list['ListAllEnvelopeRecipientsTabsCompanyTabsArrayItemRef']]):
        currency_tabs (Optional[list['ListAllEnvelopeRecipientsTabsCurrencyTabsArrayItemRef']]):
        date_signed_tabs (Optional[list['ListAllEnvelopeRecipientsTabsDateSignedTabsArrayItemRef']]):
        date_tabs (Optional[list['ListAllEnvelopeRecipientsTabsDateTabsArrayItemRef']]):
        decline_tabs (Optional[list['ListAllEnvelopeRecipientsTabsDeclineTabsArrayItemRef']]):
        draw_tabs (Optional[list['ListAllEnvelopeRecipientsTabsDrawTabsArrayItemRef']]):
        email_address_tabs (Optional[list['ListAllEnvelopeRecipientsTabsEmailAddressTabsArrayItemRef']]):
        email_tabs (Optional[list['ListAllEnvelopeRecipientsTabsEmailTabsArrayItemRef']]):
        envelope_id_tabs (Optional[list['ListAllEnvelopeRecipientsTabsEnvelopeIdTabsArrayItemRef']]):
        first_name_tabs (Optional[list['ListAllEnvelopeRecipientsTabsFirstNameTabsArrayItemRef']]):
        formula_tabs (Optional[list['ListAllEnvelopeRecipientsTabsFormulaTabsArrayItemRef']]):
        full_name_tabs (Optional[list['ListAllEnvelopeRecipientsTabsFullNameTabsArrayItemRef']]):
        initial_here_tabs (Optional[list['ListAllEnvelopeRecipientsTabsInitialHereTabsArrayItemRef']]):
        last_name_tabs (Optional[list['ListAllEnvelopeRecipientsTabsLastNameTabsArrayItemRef']]):
        list_tabs (Optional[list['ListAllEnvelopeRecipientsTabsListTabsArrayItemRef']]):
        notarize_tabs (Optional[list['ListAllEnvelopeRecipientsTabsNotarizeTabsArrayItemRef']]):
        notary_seal_tabs (Optional[list['ListAllEnvelopeRecipientsTabsNotarySealTabsArrayItemRef']]):
        note_tabs (Optional[list['ListAllEnvelopeRecipientsTabsNoteTabsArrayItemRef']]):
        number_tabs (Optional[list['ListAllEnvelopeRecipientsTabsNumberTabsArrayItemRef']]):
        phone_number_tabs (Optional[list['ListAllEnvelopeRecipientsTabsPhoneNumberTabsArrayItemRef']]):
        poly_line_overlay_tabs (Optional[list['ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsArrayItemRef']]):
        prefill_tabs (Optional[ListAllEnvelopeRecipientsTabsPrefillTabs]):
        radio_group_tabs (Optional[list['ListAllEnvelopeRecipientsTabsRadioGroupTabsArrayItemRef']]):
        sign_here_tabs (Optional[list['ListAllEnvelopeRecipientsTabsSignHereTabsArrayItemRef']]):
        signer_attachment_tabs (Optional[list['ListAllEnvelopeRecipientsTabsSignerAttachmentTabsArrayItemRef']]):
        smart_section_tabs (Optional[list['ListAllEnvelopeRecipientsTabsSmartSectionTabsArrayItemRef']]):
        ssn_tabs (Optional[list['ListAllEnvelopeRecipientsTabsSsnTabsArrayItemRef']]):
        tab_groups (Optional[list['ListAllEnvelopeRecipientsTabsTabGroupsArrayItemRef']]):
        text_tabs (Optional[list['ListAllEnvelopeRecipientsTabsTextTabsArrayItemRef']]):
        title_tabs (Optional[list['ListAllEnvelopeRecipientsTabsTitleTabsArrayItemRef']]):
        view_tabs (Optional[list['ListAllEnvelopeRecipientsTabsViewTabsArrayItemRef']]):
        zip_tabs (Optional[list['ListAllEnvelopeRecipientsTabsZipTabsArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    approve_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsApproveTabsArrayItemRef"]
    ] = Field(alias="approveTabs", default=None)
    checkbox_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCheckboxTabsArrayItemRef"]
    ] = Field(alias="checkboxTabs", default=None)
    comment_thread_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCommentThreadTabsArrayItemRef"]
    ] = Field(alias="commentThreadTabs", default=None)
    commission_county_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCommissionCountyTabsArrayItemRef"]
    ] = Field(alias="commissionCountyTabs", default=None)
    commission_expiration_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCommissionExpirationTabsArrayItemRef"]
    ] = Field(alias="commissionExpirationTabs", default=None)
    commission_number_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCommissionNumberTabsArrayItemRef"]
    ] = Field(alias="commissionNumberTabs", default=None)
    commission_state_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCommissionStateTabsArrayItemRef"]
    ] = Field(alias="commissionStateTabs", default=None)
    company_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCompanyTabsArrayItemRef"]
    ] = Field(alias="companyTabs", default=None)
    currency_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsCurrencyTabsArrayItemRef"]
    ] = Field(alias="currencyTabs", default=None)
    date_signed_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsDateSignedTabsArrayItemRef"]
    ] = Field(alias="dateSignedTabs", default=None)
    date_tabs: Optional[list["ListAllEnvelopeRecipientsTabsDateTabsArrayItemRef"]] = (
        Field(alias="dateTabs", default=None)
    )
    decline_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsDeclineTabsArrayItemRef"]
    ] = Field(alias="declineTabs", default=None)
    draw_tabs: Optional[list["ListAllEnvelopeRecipientsTabsDrawTabsArrayItemRef"]] = (
        Field(alias="drawTabs", default=None)
    )
    email_address_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsEmailAddressTabsArrayItemRef"]
    ] = Field(alias="emailAddressTabs", default=None)
    email_tabs: Optional[list["ListAllEnvelopeRecipientsTabsEmailTabsArrayItemRef"]] = (
        Field(alias="emailTabs", default=None)
    )
    envelope_id_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsEnvelopeIdTabsArrayItemRef"]
    ] = Field(alias="envelopeIdTabs", default=None)
    first_name_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsFirstNameTabsArrayItemRef"]
    ] = Field(alias="firstNameTabs", default=None)
    formula_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsFormulaTabsArrayItemRef"]
    ] = Field(alias="formulaTabs", default=None)
    full_name_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsFullNameTabsArrayItemRef"]
    ] = Field(alias="fullNameTabs", default=None)
    initial_here_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsInitialHereTabsArrayItemRef"]
    ] = Field(alias="initialHereTabs", default=None)
    last_name_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsLastNameTabsArrayItemRef"]
    ] = Field(alias="lastNameTabs", default=None)
    list_tabs: Optional[list["ListAllEnvelopeRecipientsTabsListTabsArrayItemRef"]] = (
        Field(alias="listTabs", default=None)
    )
    notarize_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsNotarizeTabsArrayItemRef"]
    ] = Field(alias="notarizeTabs", default=None)
    notary_seal_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsNotarySealTabsArrayItemRef"]
    ] = Field(alias="notarySealTabs", default=None)
    note_tabs: Optional[list["ListAllEnvelopeRecipientsTabsNoteTabsArrayItemRef"]] = (
        Field(alias="noteTabs", default=None)
    )
    number_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsNumberTabsArrayItemRef"]
    ] = Field(alias="numberTabs", default=None)
    phone_number_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsPhoneNumberTabsArrayItemRef"]
    ] = Field(alias="phoneNumberTabs", default=None)
    poly_line_overlay_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsPolyLineOverlayTabsArrayItemRef"]
    ] = Field(alias="polyLineOverlayTabs", default=None)
    prefill_tabs: Optional["ListAllEnvelopeRecipientsTabsPrefillTabs"] = Field(
        alias="prefillTabs", default=None
    )
    radio_group_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsRadioGroupTabsArrayItemRef"]
    ] = Field(alias="radioGroupTabs", default=None)
    sign_here_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsSignHereTabsArrayItemRef"]
    ] = Field(alias="signHereTabs", default=None)
    signer_attachment_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsSignerAttachmentTabsArrayItemRef"]
    ] = Field(alias="signerAttachmentTabs", default=None)
    smart_section_tabs: Optional[
        list["ListAllEnvelopeRecipientsTabsSmartSectionTabsArrayItemRef"]
    ] = Field(alias="smartSectionTabs", default=None)
    ssn_tabs: Optional[list["ListAllEnvelopeRecipientsTabsSsnTabsArrayItemRef"]] = (
        Field(alias="ssnTabs", default=None)
    )
    tab_groups: Optional[list["ListAllEnvelopeRecipientsTabsTabGroupsArrayItemRef"]] = (
        Field(alias="tabGroups", default=None)
    )
    text_tabs: Optional[list["ListAllEnvelopeRecipientsTabsTextTabsArrayItemRef"]] = (
        Field(alias="textTabs", default=None)
    )
    title_tabs: Optional[list["ListAllEnvelopeRecipientsTabsTitleTabsArrayItemRef"]] = (
        Field(alias="titleTabs", default=None)
    )
    view_tabs: Optional[list["ListAllEnvelopeRecipientsTabsViewTabsArrayItemRef"]] = (
        Field(alias="viewTabs", default=None)
    )
    zip_tabs: Optional[list["ListAllEnvelopeRecipientsTabsZipTabsArrayItemRef"]] = (
        Field(alias="zipTabs", default=None)
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListAllEnvelopeRecipientsTabs"], src_dict: Dict[str, Any]):
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
