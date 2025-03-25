from .curated_add_document_to_envelope import (
    add_document_to_envelope as _add_document_to_envelope,
    add_document_to_envelope_async as _add_document_to_envelope_async,
)
from ..models.add_document_to_envelope_body import AddDocumentToEnvelopeBody
from ..models.add_document_to_envelope_request import AddDocumentToEnvelopeRequest
from ..models.add_document_to_envelope_response import AddDocumentToEnvelopeResponse
from ..models.default_error import DefaultError
from typing import cast
from .curated_add_recipient_to_envelope import (
    add_recipient_to_envelope as _add_recipient_to_envelope,
    add_recipient_to_envelope_async as _add_recipient_to_envelope_async,
)
from ..models.add_recipient_to_envelope_request import AddRecipientToEnvelopeRequest
from ..models.add_recipient_to_envelope_response import AddRecipientToEnvelopeResponse
from .curated_create_envelope_by_clone import (
    create_by_copying_envelope as _create_by_copying_envelope,
    create_by_copying_envelope_async as _create_by_copying_envelope_async,
)
from ..models.create_by_copying_envelope_request import CreateByCopyingEnvelopeRequest
from ..models.create_by_copying_envelope_response import CreateByCopyingEnvelopeResponse
from .create_envelope import (
    create_envelope as _create_envelope,
    create_envelope_async as _create_envelope_async,
)
from ..models.create_envelope_body import CreateEnvelopeBody
from ..models.create_envelope_request import CreateEnvelopeRequest
from ..models.create_envelope_response import CreateEnvelopeResponse
from .curated_create_envelope_by_template import (
    create_envelope_using_template as _create_envelope_using_template,
    create_envelope_using_template_async as _create_envelope_using_template_async,
)
from ..models.create_envelope_using_template_request import (
    CreateEnvelopeUsingTemplateRequest,
)
from ..models.create_envelope_using_template_response import (
    CreateEnvelopeUsingTemplateResponse,
)
from .download_envelope_documents import (
    download_documents_of_envelope as _download_documents_of_envelope,
    download_documents_of_envelope_async as _download_documents_of_envelope_async,
)
from ..models.download_documents_of_envelope_response import (
    DownloadDocumentsOfEnvelopeResponse,
)
from ..types import File
from io import BytesIO
from .envelopes import (
    get_envelope as _get_envelope,
    get_envelope_async as _get_envelope_async,
)
from ..models.get_envelope_response import GetEnvelopeResponse
from .envelopesform_data import (
    get_form_data as _get_form_data,
    get_form_data_async as _get_form_data_async,
)
from ..models.get_form_data_response import GetFormDataResponse
from .templates import (
    get_template as _get_template,
    get_template_async as _get_template_async,
)
from ..models.get_template_response import GetTemplateResponse
from .curated_envelopes_recipients import (
    list_all_envelope_recipients as _list_all_envelope_recipients,
    list_all_envelope_recipients_async as _list_all_envelope_recipients_async,
)
from ..models.list_all_envelope_recipients import ListAllEnvelopeRecipients
from .curated_send_envelope import (
    send_envelope as _send_envelope,
    send_envelope_async as _send_envelope_async,
)
from ..models.send_envelope_response import SendEnvelopeResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class DocusignDocusign:
    def __init__(self, *, instance_id: str, client: httpx.Client):
        base_url = str(client.base_url).rstrip("/")
        new_headers = {
            k: v for k, v in client.headers.items() if k not in ["content-type"]
        }
        new_client = httpx.Client(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        new_client_async = httpx.AsyncClient(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        self.client = (
            Client(
                base_url="",  # this will be overridden by the base_url in the Client constructor
            )
            .set_httpx_client(new_client)
            .set_async_httpx_client(new_client_async)
        )

    def add_document_to_envelope(
        self,
        *,
        body: AddDocumentToEnvelopeBody,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[AddDocumentToEnvelopeResponse, DefaultError]]:
        return _add_document_to_envelope(
            client=self.client,
            body=body,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )

    async def add_document_to_envelope_async(
        self,
        *,
        body: AddDocumentToEnvelopeBody,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[AddDocumentToEnvelopeResponse, DefaultError]]:
        return await _add_document_to_envelope_async(
            client=self.client,
            body=body,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )

    def add_recipient_to_envelope(
        self,
        *,
        body: AddRecipientToEnvelopeRequest,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[AddRecipientToEnvelopeResponse, DefaultError]]:
        return _add_recipient_to_envelope(
            client=self.client,
            body=body,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )

    async def add_recipient_to_envelope_async(
        self,
        *,
        body: AddRecipientToEnvelopeRequest,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[AddRecipientToEnvelopeResponse, DefaultError]]:
        return await _add_recipient_to_envelope_async(
            client=self.client,
            body=body,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )

    def create_by_copying_envelope(
        self,
        *,
        body: CreateByCopyingEnvelopeRequest,
    ) -> Optional[Union[CreateByCopyingEnvelopeResponse, DefaultError]]:
        return _create_by_copying_envelope(
            client=self.client,
            body=body,
        )

    async def create_by_copying_envelope_async(
        self,
        *,
        body: CreateByCopyingEnvelopeRequest,
    ) -> Optional[Union[CreateByCopyingEnvelopeResponse, DefaultError]]:
        return await _create_by_copying_envelope_async(
            client=self.client,
            body=body,
        )

    def create_envelope(
        self,
        *,
        body: CreateEnvelopeBody,
    ) -> Optional[Union[CreateEnvelopeResponse, DefaultError]]:
        return _create_envelope(
            client=self.client,
            body=body,
        )

    async def create_envelope_async(
        self,
        *,
        body: CreateEnvelopeBody,
    ) -> Optional[Union[CreateEnvelopeResponse, DefaultError]]:
        return await _create_envelope_async(
            client=self.client,
            body=body,
        )

    def create_envelope_using_template(
        self,
        *,
        body: CreateEnvelopeUsingTemplateRequest,
    ) -> Optional[Union[CreateEnvelopeUsingTemplateResponse, DefaultError]]:
        return _create_envelope_using_template(
            client=self.client,
            body=body,
        )

    async def create_envelope_using_template_async(
        self,
        *,
        body: CreateEnvelopeUsingTemplateRequest,
    ) -> Optional[Union[CreateEnvelopeUsingTemplateResponse, DefaultError]]:
        return await _create_envelope_using_template_async(
            client=self.client,
            body=body,
        )

    def download_documents_of_envelope(
        self,
        *,
        envelope_id: str,
        envelope_id_lookup: Any,
        download_type: Optional[str] = None,
        document_id: Optional[str] = None,
        certificate: Optional[bool] = None,
    ) -> Optional[Union[DefaultError, File]]:
        return _download_documents_of_envelope(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            download_type=download_type,
            document_id=document_id,
            certificate=certificate,
        )

    async def download_documents_of_envelope_async(
        self,
        *,
        envelope_id: str,
        envelope_id_lookup: Any,
        download_type: Optional[str] = None,
        document_id: Optional[str] = None,
        certificate: Optional[bool] = None,
    ) -> Optional[Union[DefaultError, File]]:
        return await _download_documents_of_envelope_async(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            download_type=download_type,
            document_id=document_id,
            certificate=certificate,
        )

    def get_envelope(
        self,
        envelope_id_lookup: Any,
        envelope_id: str,
        *,
        advanced_update: Optional[str] = None,
        include: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetEnvelopeResponse]]:
        return _get_envelope(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            advanced_update=advanced_update,
            include=include,
        )

    async def get_envelope_async(
        self,
        envelope_id_lookup: Any,
        envelope_id: str,
        *,
        advanced_update: Optional[str] = None,
        include: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetEnvelopeResponse]]:
        return await _get_envelope_async(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            advanced_update=advanced_update,
            include=include,
        )

    def get_form_data(
        self,
        envelope_id_lookup: Any,
        envelope_id: str,
        *,
        fields: Optional[str] = None,
        order_by: Optional[str] = None,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetFormDataResponse]]:
        return _get_form_data(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            fields=fields,
            order_by=order_by,
            page_size=page_size,
            next_page=next_page,
        )

    async def get_form_data_async(
        self,
        envelope_id_lookup: Any,
        envelope_id: str,
        *,
        fields: Optional[str] = None,
        order_by: Optional[str] = None,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetFormDataResponse]]:
        return await _get_form_data_async(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            fields=fields,
            order_by=order_by,
            page_size=page_size,
            next_page=next_page,
        )

    def get_template(
        self,
        template_id_lookup: Any,
        template_id: str,
        *,
        include: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetTemplateResponse]]:
        return _get_template(
            client=self.client,
            template_id=template_id,
            template_id_lookup=template_id_lookup,
            include=include,
        )

    async def get_template_async(
        self,
        template_id_lookup: Any,
        template_id: str,
        *,
        include: Optional[str] = None,
    ) -> Optional[Union[DefaultError, GetTemplateResponse]]:
        return await _get_template_async(
            client=self.client,
            template_id=template_id,
            template_id_lookup=template_id_lookup,
            include=include,
        )

    def list_all_envelope_recipients(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        include_anchor_tab_locations: Optional[bool] = None,
        include_metadata: Optional[bool] = None,
        include_tabs: Optional[bool] = None,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[DefaultError, list["ListAllEnvelopeRecipients"]]]:
        return _list_all_envelope_recipients(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            include_anchor_tab_locations=include_anchor_tab_locations,
            include_metadata=include_metadata,
            include_tabs=include_tabs,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )

    async def list_all_envelope_recipients_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        include_anchor_tab_locations: Optional[bool] = None,
        include_metadata: Optional[bool] = None,
        include_tabs: Optional[bool] = None,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[DefaultError, list["ListAllEnvelopeRecipients"]]]:
        return await _list_all_envelope_recipients_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            include_anchor_tab_locations=include_anchor_tab_locations,
            include_metadata=include_metadata,
            include_tabs=include_tabs,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )

    def send_envelope(
        self,
        *,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[DefaultError, SendEnvelopeResponse]]:
        return _send_envelope(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )

    async def send_envelope_async(
        self,
        *,
        envelope_id: str,
        envelope_id_lookup: Any,
    ) -> Optional[Union[DefaultError, SendEnvelopeResponse]]:
        return await _send_envelope_async(
            client=self.client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
        )
