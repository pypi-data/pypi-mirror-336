from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_template_response import GetTemplateResponse


def _get_kwargs(
    template_id: str,
    *,
    include: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include"] = include

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/templates/{template_id}".format(
            template_id=template_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, GetTemplateResponse]]:
    if response.status_code == 200:
        response_200 = GetTemplateResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, GetTemplateResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id_lookup: Any,
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Optional[str] = None,
) -> Response[Union[DefaultError, GetTemplateResponse]]:
    """Get Template

     Retrieve the definition of a template

    Args:
        template_id (str): Type the name or ID of the template. If the template is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            templates and then type the template or retrieve the template ID from 'List All
            Records->Templates'
        include (Optional[str]): A comma-separated list of additional template attributes to
            include in the response. Valid values are: powerforms →  Includes information about
            PowerForms, tabs → Includes information about tabs, documents → Includes information about
            documents, favorite_template_status → Includes the template favoritedByMe property in the
            response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetTemplateResponse]]
    """

    if not template_id and template_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/templates"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if (
                template_id_lookup in item["name"]
                or template_id_lookup in item["templateId"]
            ):
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for template_id_lookup in templates")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for template_id_lookup in templates. Using the first match."
            )

        template_id = found_items[0]["templateId"]

    kwargs = _get_kwargs(
        template_id=template_id,
        include=include,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    template_id_lookup: Any,
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Optional[str] = None,
) -> Optional[Union[DefaultError, GetTemplateResponse]]:
    """Get Template

     Retrieve the definition of a template

    Args:
        template_id (str): Type the name or ID of the template. If the template is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            templates and then type the template or retrieve the template ID from 'List All
            Records->Templates'
        include (Optional[str]): A comma-separated list of additional template attributes to
            include in the response. Valid values are: powerforms →  Includes information about
            PowerForms, tabs → Includes information about tabs, documents → Includes information about
            documents, favorite_template_status → Includes the template favoritedByMe property in the
            response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetTemplateResponse]
    """

    return sync_detailed(
        template_id=template_id,
        template_id_lookup=template_id_lookup,
        client=client,
        include=include,
    ).parsed


async def asyncio_detailed(
    template_id_lookup: Any,
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Optional[str] = None,
) -> Response[Union[DefaultError, GetTemplateResponse]]:
    """Get Template

     Retrieve the definition of a template

    Args:
        template_id (str): Type the name or ID of the template. If the template is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            templates and then type the template or retrieve the template ID from 'List All
            Records->Templates'
        include (Optional[str]): A comma-separated list of additional template attributes to
            include in the response. Valid values are: powerforms →  Includes information about
            PowerForms, tabs → Includes information about tabs, documents → Includes information about
            documents, favorite_template_status → Includes the template favoritedByMe property in the
            response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetTemplateResponse]]
    """

    if not template_id and template_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/templates"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if (
                template_id_lookup in item["name"]
                or template_id_lookup in item["templateId"]
            ):
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for template_id_lookup in templates")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for template_id_lookup in templates. Using the first match."
            )

        template_id = found_items[0]["templateId"]

    kwargs = _get_kwargs(
        template_id=template_id,
        include=include,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_id_lookup: Any,
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include: Optional[str] = None,
) -> Optional[Union[DefaultError, GetTemplateResponse]]:
    """Get Template

     Retrieve the definition of a template

    Args:
        template_id (str): Type the name or ID of the template. If the template is not found in
            the drop-down, you can first scroll the drop-down till the bottom to get all the available
            templates and then type the template or retrieve the template ID from 'List All
            Records->Templates'
        include (Optional[str]): A comma-separated list of additional template attributes to
            include in the response. Valid values are: powerforms →  Includes information about
            PowerForms, tabs → Includes information about tabs, documents → Includes information about
            documents, favorite_template_status → Includes the template favoritedByMe property in the
            response.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetTemplateResponse]
    """

    return (
        await asyncio_detailed(
            template_id=template_id,
            template_id_lookup=template_id_lookup,
            client=client,
            include=include,
        )
    ).parsed
