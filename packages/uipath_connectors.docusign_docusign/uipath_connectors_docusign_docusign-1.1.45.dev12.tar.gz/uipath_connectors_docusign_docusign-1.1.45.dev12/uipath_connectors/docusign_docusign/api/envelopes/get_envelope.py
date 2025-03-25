from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_envelope_response import GetEnvelopeResponse


def _get_kwargs(
    envelope_id: str,
    *,
    advanced_update: Optional[str] = None,
    include: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["advanced_update"] = advanced_update

    params["include"] = include

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/envelopes/{envelope_id}".format(
            envelope_id=envelope_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, GetEnvelopeResponse]]:
    if response.status_code == 200:
        response_200 = GetEnvelopeResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, GetEnvelopeResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    envelope_id_lookup: Any,
    envelope_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    advanced_update: Optional[str] = None,
    include: Optional[str] = None,
) -> Response[Union[DefaultError, GetEnvelopeResponse]]:
    """Get Envelope

     Retrieve the envelope status

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> 'Manage' tab -> Goto “Sent” or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is '3ae67e54-f761-4a5b-a23e-b5e4835492cc'
        advanced_update (Optional[str]): When **true**, envelope information can be added or
            modified.
        include (Optional[str]): Specifies additional information about the envelope to return.
            Enter a comma-separated list, such as `tabs,recipients`. Valid values are:-
            `custom_fields`: The custom fields associated with the envelope.- `documents`: The
            documents associated with the envelope.- `attachments`: The attachments associated with
            the envelope.- `extensions`: Information about the email settings associated with the
            envelope.- `folders`: The folder where the envelope exists.- `recipients`: The recipients
            associated with the envelope.- `powerform`: The PowerForms associated with the envelope.-
            `tabs`: The tabs associated with the envelope.- `payment_tabs`: The payment tabs
            associated with the envelope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetEnvelopeResponse]]
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
        advanced_update=advanced_update,
        include=include,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    envelope_id_lookup: Any,
    envelope_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    advanced_update: Optional[str] = None,
    include: Optional[str] = None,
) -> Optional[Union[DefaultError, GetEnvelopeResponse]]:
    """Get Envelope

     Retrieve the envelope status

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> 'Manage' tab -> Goto “Sent” or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is '3ae67e54-f761-4a5b-a23e-b5e4835492cc'
        advanced_update (Optional[str]): When **true**, envelope information can be added or
            modified.
        include (Optional[str]): Specifies additional information about the envelope to return.
            Enter a comma-separated list, such as `tabs,recipients`. Valid values are:-
            `custom_fields`: The custom fields associated with the envelope.- `documents`: The
            documents associated with the envelope.- `attachments`: The attachments associated with
            the envelope.- `extensions`: Information about the email settings associated with the
            envelope.- `folders`: The folder where the envelope exists.- `recipients`: The recipients
            associated with the envelope.- `powerform`: The PowerForms associated with the envelope.-
            `tabs`: The tabs associated with the envelope.- `payment_tabs`: The payment tabs
            associated with the envelope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetEnvelopeResponse]
    """

    return sync_detailed(
        envelope_id=envelope_id,
        envelope_id_lookup=envelope_id_lookup,
        client=client,
        advanced_update=advanced_update,
        include=include,
    ).parsed


async def asyncio_detailed(
    envelope_id_lookup: Any,
    envelope_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    advanced_update: Optional[str] = None,
    include: Optional[str] = None,
) -> Response[Union[DefaultError, GetEnvelopeResponse]]:
    """Get Envelope

     Retrieve the envelope status

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> 'Manage' tab -> Goto “Sent” or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is '3ae67e54-f761-4a5b-a23e-b5e4835492cc'
        advanced_update (Optional[str]): When **true**, envelope information can be added or
            modified.
        include (Optional[str]): Specifies additional information about the envelope to return.
            Enter a comma-separated list, such as `tabs,recipients`. Valid values are:-
            `custom_fields`: The custom fields associated with the envelope.- `documents`: The
            documents associated with the envelope.- `attachments`: The attachments associated with
            the envelope.- `extensions`: Information about the email settings associated with the
            envelope.- `folders`: The folder where the envelope exists.- `recipients`: The recipients
            associated with the envelope.- `powerform`: The PowerForms associated with the envelope.-
            `tabs`: The tabs associated with the envelope.- `payment_tabs`: The payment tabs
            associated with the envelope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetEnvelopeResponse]]
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
        advanced_update=advanced_update,
        include=include,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    envelope_id_lookup: Any,
    envelope_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    advanced_update: Optional[str] = None,
    include: Optional[str] = None,
) -> Optional[Union[DefaultError, GetEnvelopeResponse]]:
    """Get Envelope

     Retrieve the envelope status

    Args:
        envelope_id (str): Type the name or ID of the envelope. If the envelope is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            envelopes and then type the envelope or retrieve the envelope ID from the DocuSign
            application -> 'Manage' tab -> Goto “Sent” or “Draft” under “Envelopes” -> Click on the
            respective envelope and retrieve the envelope ID from URL. For example, if the URL is
            “https://appdemo.docusign.com/documents/details/3ae67e54-f761-4a5b-a23e-b5e4835492cc”, the
            envelope ID is '3ae67e54-f761-4a5b-a23e-b5e4835492cc'
        advanced_update (Optional[str]): When **true**, envelope information can be added or
            modified.
        include (Optional[str]): Specifies additional information about the envelope to return.
            Enter a comma-separated list, such as `tabs,recipients`. Valid values are:-
            `custom_fields`: The custom fields associated with the envelope.- `documents`: The
            documents associated with the envelope.- `attachments`: The attachments associated with
            the envelope.- `extensions`: Information about the email settings associated with the
            envelope.- `folders`: The folder where the envelope exists.- `recipients`: The recipients
            associated with the envelope.- `powerform`: The PowerForms associated with the envelope.-
            `tabs`: The tabs associated with the envelope.- `payment_tabs`: The payment tabs
            associated with the envelope.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetEnvelopeResponse]
    """

    return (
        await asyncio_detailed(
            envelope_id=envelope_id,
            envelope_id_lookup=envelope_id_lookup,
            client=client,
            advanced_update=advanced_update,
            include=include,
        )
    ).parsed
