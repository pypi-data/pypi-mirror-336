from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...types import File
from io import BytesIO


def _get_kwargs(
    *,
    envelope_id: str,
    download_type: Optional[str] = None,
    document_id: Optional[str] = None,
    certificate: Optional[bool] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["envelopeId"] = envelope_id

    params["downloadType"] = download_type

    params["documentId"] = document_id

    params["certificate"] = certificate

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/downloadEnvelopeDocuments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, File]]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200
    if response.status_code == 400:
        response_400 = DefaultError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = DefaultError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = DefaultError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = DefaultError.from_dict(response.json())

        return response_404
    if response.status_code == 405:
        response_405 = DefaultError.from_dict(response.json())

        return response_405
    if response.status_code == 406:
        response_406 = DefaultError.from_dict(response.json())

        return response_406
    if response.status_code == 409:
        response_409 = DefaultError.from_dict(response.json())

        return response_409
    if response.status_code == 415:
        response_415 = DefaultError.from_dict(response.json())

        return response_415
    if response.status_code == 500:
        response_500 = DefaultError.from_dict(response.json())

        return response_500
    if response.status_code == 402:
        response_402 = DefaultError.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DefaultError, File]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    envelope_id: str,
    envelope_id_lookup: Any,
    download_type: Optional[str] = None,
    document_id: Optional[str] = None,
    certificate: Optional[bool] = None,
) -> Response[Union[DefaultError, File]]:
    """Download Documents of Envelope

     Download all the documents of an envelope in DocuSign

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> "Manage" tab -> Goto "Sent" or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is “3ae67e54-f761-4a5b-a23e-b5e4835492cc”
        download_type (Optional[str]): Can take one of the following values i.e. “combined” for
            retrieving all documents as a single PDF file, “archive” for retrieving a ZIP archive that
            contains all of the PDF documents, “certificate” for retrieving only the certificate of
            completion and “portfolio” for retrieving the envelope documents as a PDF portfolio.
        document_id (Optional[str]): Select document ID from the dropdown to download. If both
            documentId and download type are passed, document ID will be honoured.
        certificate (Optional[bool]): Used only when the Download type is “combined”. When true,
            the certificate of completion is included in the combined PDF file. Default is false.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, File]]
    """

    if not envelope_id and envelope_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get",
            url="/envelopes_dtl?from_date=2000-01-01&status=created,sent,completed",
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if (
                envelope_id_lookup in item["emailSubject"]
                or envelope_id_lookup in item["envelopeId"]
            ):
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for envelope_id_lookup in envelopes_dtl?from_date=2000-01-01&status=created,sent,completed"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for envelope_id_lookup in envelopes_dtl?from_date=2000-01-01&status=created,sent,completed. Using the first match."
            )

        envelope_id = found_items[0]["envelopeId"]

    kwargs = _get_kwargs(
        envelope_id=envelope_id,
        download_type=download_type,
        document_id=document_id,
        certificate=certificate,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    envelope_id: str,
    envelope_id_lookup: Any,
    download_type: Optional[str] = None,
    document_id: Optional[str] = None,
    certificate: Optional[bool] = None,
) -> Optional[Union[DefaultError, File]]:
    """Download Documents of Envelope

     Download all the documents of an envelope in DocuSign

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> "Manage" tab -> Goto "Sent" or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is “3ae67e54-f761-4a5b-a23e-b5e4835492cc”
        download_type (Optional[str]): Can take one of the following values i.e. “combined” for
            retrieving all documents as a single PDF file, “archive” for retrieving a ZIP archive that
            contains all of the PDF documents, “certificate” for retrieving only the certificate of
            completion and “portfolio” for retrieving the envelope documents as a PDF portfolio.
        document_id (Optional[str]): Select document ID from the dropdown to download. If both
            documentId and download type are passed, document ID will be honoured.
        certificate (Optional[bool]): Used only when the Download type is “combined”. When true,
            the certificate of completion is included in the combined PDF file. Default is false.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, File]
    """

    return sync_detailed(
        client=client,
        envelope_id=envelope_id,
        envelope_id_lookup=envelope_id_lookup,
        download_type=download_type,
        document_id=document_id,
        certificate=certificate,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    envelope_id: str,
    envelope_id_lookup: Any,
    download_type: Optional[str] = None,
    document_id: Optional[str] = None,
    certificate: Optional[bool] = None,
) -> Response[Union[DefaultError, File]]:
    """Download Documents of Envelope

     Download all the documents of an envelope in DocuSign

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> "Manage" tab -> Goto "Sent" or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is “3ae67e54-f761-4a5b-a23e-b5e4835492cc”
        download_type (Optional[str]): Can take one of the following values i.e. “combined” for
            retrieving all documents as a single PDF file, “archive” for retrieving a ZIP archive that
            contains all of the PDF documents, “certificate” for retrieving only the certificate of
            completion and “portfolio” for retrieving the envelope documents as a PDF portfolio.
        document_id (Optional[str]): Select document ID from the dropdown to download. If both
            documentId and download type are passed, document ID will be honoured.
        certificate (Optional[bool]): Used only when the Download type is “combined”. When true,
            the certificate of completion is included in the combined PDF file. Default is false.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, File]]
    """

    if not envelope_id and envelope_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get",
            url="/envelopes_dtl?from_date=2000-01-01&status=created,sent,completed",
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if (
                envelope_id_lookup in item["emailSubject"]
                or envelope_id_lookup in item["envelopeId"]
            ):
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for envelope_id_lookup in envelopes_dtl?from_date=2000-01-01&status=created,sent,completed"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for envelope_id_lookup in envelopes_dtl?from_date=2000-01-01&status=created,sent,completed. Using the first match."
            )

        envelope_id = found_items[0]["envelopeId"]

    kwargs = _get_kwargs(
        envelope_id=envelope_id,
        download_type=download_type,
        document_id=document_id,
        certificate=certificate,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    envelope_id: str,
    envelope_id_lookup: Any,
    download_type: Optional[str] = None,
    document_id: Optional[str] = None,
    certificate: Optional[bool] = None,
) -> Optional[Union[DefaultError, File]]:
    """Download Documents of Envelope

     Download all the documents of an envelope in DocuSign

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> "Manage" tab -> Goto "Sent" or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is “3ae67e54-f761-4a5b-a23e-b5e4835492cc”
        download_type (Optional[str]): Can take one of the following values i.e. “combined” for
            retrieving all documents as a single PDF file, “archive” for retrieving a ZIP archive that
            contains all of the PDF documents, “certificate” for retrieving only the certificate of
            completion and “portfolio” for retrieving the envelope documents as a PDF portfolio.
        document_id (Optional[str]): Select document ID from the dropdown to download. If both
            documentId and download type are passed, document ID will be honoured.
        certificate (Optional[bool]): Used only when the Download type is “combined”. When true,
            the certificate of completion is included in the combined PDF file. Default is false.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, File]
    """

    return (
        await asyncio_detailed(
            client=client,
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            download_type=download_type,
            document_id=document_id,
            certificate=certificate,
        )
    ).parsed
