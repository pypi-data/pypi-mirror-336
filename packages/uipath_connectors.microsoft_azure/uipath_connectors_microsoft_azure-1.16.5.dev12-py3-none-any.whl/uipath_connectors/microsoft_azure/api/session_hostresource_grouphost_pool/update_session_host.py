from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.update_session_host_response import UpdateSessionHostResponse


def _get_kwargs(
    session_host_name: str,
    resource_group_name: str,
    host_pool_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/sessionHost/{session_host_name}/resourceGroup/{resource_group_name}/hostPool/{host_pool_name}".format(
            session_host_name=session_host_name,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, UpdateSessionHostResponse]]:
    if response.status_code == 200:
        response_200 = UpdateSessionHostResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, UpdateSessionHostResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_host_name: str,
    resource_group_name: str,
    host_pool_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DefaultError, UpdateSessionHostResponse]]:
    """Update Session Host

     Updates a session host.

    Args:
        session_host_name (str): The session host on which the operation is performed.
        resource_group_name (str): The name of the resource group to which the host pool belongs.
        host_pool_name (str): The host pool to which the session host belongs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateSessionHostResponse]]
    """

    kwargs = _get_kwargs(
        session_host_name=session_host_name,
        resource_group_name=resource_group_name,
        host_pool_name=host_pool_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_host_name: str,
    resource_group_name: str,
    host_pool_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DefaultError, UpdateSessionHostResponse]]:
    """Update Session Host

     Updates a session host.

    Args:
        session_host_name (str): The session host on which the operation is performed.
        resource_group_name (str): The name of the resource group to which the host pool belongs.
        host_pool_name (str): The host pool to which the session host belongs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateSessionHostResponse]
    """

    return sync_detailed(
        session_host_name=session_host_name,
        resource_group_name=resource_group_name,
        host_pool_name=host_pool_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    session_host_name: str,
    resource_group_name: str,
    host_pool_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DefaultError, UpdateSessionHostResponse]]:
    """Update Session Host

     Updates a session host.

    Args:
        session_host_name (str): The session host on which the operation is performed.
        resource_group_name (str): The name of the resource group to which the host pool belongs.
        host_pool_name (str): The host pool to which the session host belongs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateSessionHostResponse]]
    """

    kwargs = _get_kwargs(
        session_host_name=session_host_name,
        resource_group_name=resource_group_name,
        host_pool_name=host_pool_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_host_name: str,
    resource_group_name: str,
    host_pool_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DefaultError, UpdateSessionHostResponse]]:
    """Update Session Host

     Updates a session host.

    Args:
        session_host_name (str): The session host on which the operation is performed.
        resource_group_name (str): The name of the resource group to which the host pool belongs.
        host_pool_name (str): The host pool to which the session host belongs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateSessionHostResponse]
    """

    return (
        await asyncio_detailed(
            session_host_name=session_host_name,
            resource_group_name=resource_group_name,
            host_pool_name=host_pool_name,
            client=client,
        )
    ).parsed
