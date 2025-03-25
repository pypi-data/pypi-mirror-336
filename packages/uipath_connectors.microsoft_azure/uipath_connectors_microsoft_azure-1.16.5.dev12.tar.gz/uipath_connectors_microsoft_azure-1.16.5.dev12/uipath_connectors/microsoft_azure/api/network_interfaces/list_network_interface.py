from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.list_network_interface import ListNetworkInterface


def _get_kwargs(
    *,
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    resource_group_name: Optional[str] = None,
    asc_location: Optional[str] = None,
    name_starts_with: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["nextPage"] = next_page

    params["pageSize"] = page_size

    params["resourceGroupName"] = resource_group_name

    params["ascLocation"] = asc_location

    params["nameStartsWith"] = name_starts_with

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/networkInterfaces",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["ListNetworkInterface"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListNetworkInterface.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[DefaultError, list["ListNetworkInterface"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    resource_group_name: Optional[str] = None,
    asc_location: Optional[str] = None,
    name_starts_with: Optional[str] = None,
) -> Response[Union[DefaultError, list["ListNetworkInterface"]]]:
    """List Network Interface

     Lists  network interfaces

    Args:
        next_page (Optional[str]): The next page token
        page_size (Optional[int]): The number of resources to return in a given page
        resource_group_name (Optional[str]): Resource Group Name
        asc_location (Optional[str]): The location where security alert is stored.
        name_starts_with (Optional[str]): Returns only those network interfaces whose name starts
            with the

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListNetworkInterface']]]
    """

    kwargs = _get_kwargs(
        next_page=next_page,
        page_size=page_size,
        resource_group_name=resource_group_name,
        asc_location=asc_location,
        name_starts_with=name_starts_with,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    resource_group_name: Optional[str] = None,
    asc_location: Optional[str] = None,
    name_starts_with: Optional[str] = None,
) -> Optional[Union[DefaultError, list["ListNetworkInterface"]]]:
    """List Network Interface

     Lists  network interfaces

    Args:
        next_page (Optional[str]): The next page token
        page_size (Optional[int]): The number of resources to return in a given page
        resource_group_name (Optional[str]): Resource Group Name
        asc_location (Optional[str]): The location where security alert is stored.
        name_starts_with (Optional[str]): Returns only those network interfaces whose name starts
            with the

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListNetworkInterface']]
    """

    return sync_detailed(
        client=client,
        next_page=next_page,
        page_size=page_size,
        resource_group_name=resource_group_name,
        asc_location=asc_location,
        name_starts_with=name_starts_with,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    resource_group_name: Optional[str] = None,
    asc_location: Optional[str] = None,
    name_starts_with: Optional[str] = None,
) -> Response[Union[DefaultError, list["ListNetworkInterface"]]]:
    """List Network Interface

     Lists  network interfaces

    Args:
        next_page (Optional[str]): The next page token
        page_size (Optional[int]): The number of resources to return in a given page
        resource_group_name (Optional[str]): Resource Group Name
        asc_location (Optional[str]): The location where security alert is stored.
        name_starts_with (Optional[str]): Returns only those network interfaces whose name starts
            with the

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListNetworkInterface']]]
    """

    kwargs = _get_kwargs(
        next_page=next_page,
        page_size=page_size,
        resource_group_name=resource_group_name,
        asc_location=asc_location,
        name_starts_with=name_starts_with,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    resource_group_name: Optional[str] = None,
    asc_location: Optional[str] = None,
    name_starts_with: Optional[str] = None,
) -> Optional[Union[DefaultError, list["ListNetworkInterface"]]]:
    """List Network Interface

     Lists  network interfaces

    Args:
        next_page (Optional[str]): The next page token
        page_size (Optional[int]): The number of resources to return in a given page
        resource_group_name (Optional[str]): Resource Group Name
        asc_location (Optional[str]): The location where security alert is stored.
        name_starts_with (Optional[str]): Returns only those network interfaces whose name starts
            with the

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListNetworkInterface']]
    """

    return (
        await asyncio_detailed(
            client=client,
            next_page=next_page,
            page_size=page_size,
            resource_group_name=resource_group_name,
            asc_location=asc_location,
            name_starts_with=name_starts_with,
        )
    ).parsed
