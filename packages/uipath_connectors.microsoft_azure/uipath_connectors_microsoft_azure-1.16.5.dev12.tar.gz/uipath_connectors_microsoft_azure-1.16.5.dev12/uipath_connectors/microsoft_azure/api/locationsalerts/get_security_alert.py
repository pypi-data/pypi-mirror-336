from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_security_alert_response import GetSecurityAlertResponse


def _get_kwargs(
    asc_location: str,
    alert_name: str,
    *,
    resource_group_name: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["resourceGroupName"] = resource_group_name

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/locations/{asc_location}/alerts/{alert_name}".format(
            asc_location=asc_location,
            alert_name=alert_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, GetSecurityAlertResponse]]:
    if response.status_code == 200:
        response_200 = GetSecurityAlertResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, GetSecurityAlertResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    asc_location: str,
    alert_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    resource_group_name: Optional[str] = None,
) -> Response[Union[DefaultError, GetSecurityAlertResponse]]:
    """Get Security Alert

     Gets the details of a security alert at subscription or resource group level

    Args:
        asc_location (str): The location where security alert is stored.
        alert_name (str): The unique identifier(uuid) of the security alert
        resource_group_name (Optional[str]): Resource Group Name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetSecurityAlertResponse]]
    """

    kwargs = _get_kwargs(
        asc_location=asc_location,
        alert_name=alert_name,
        resource_group_name=resource_group_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    asc_location: str,
    alert_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    resource_group_name: Optional[str] = None,
) -> Optional[Union[DefaultError, GetSecurityAlertResponse]]:
    """Get Security Alert

     Gets the details of a security alert at subscription or resource group level

    Args:
        asc_location (str): The location where security alert is stored.
        alert_name (str): The unique identifier(uuid) of the security alert
        resource_group_name (Optional[str]): Resource Group Name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetSecurityAlertResponse]
    """

    return sync_detailed(
        asc_location=asc_location,
        alert_name=alert_name,
        client=client,
        resource_group_name=resource_group_name,
    ).parsed


async def asyncio_detailed(
    asc_location: str,
    alert_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    resource_group_name: Optional[str] = None,
) -> Response[Union[DefaultError, GetSecurityAlertResponse]]:
    """Get Security Alert

     Gets the details of a security alert at subscription or resource group level

    Args:
        asc_location (str): The location where security alert is stored.
        alert_name (str): The unique identifier(uuid) of the security alert
        resource_group_name (Optional[str]): Resource Group Name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetSecurityAlertResponse]]
    """

    kwargs = _get_kwargs(
        asc_location=asc_location,
        alert_name=alert_name,
        resource_group_name=resource_group_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    asc_location: str,
    alert_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    resource_group_name: Optional[str] = None,
) -> Optional[Union[DefaultError, GetSecurityAlertResponse]]:
    """Get Security Alert

     Gets the details of a security alert at subscription or resource group level

    Args:
        asc_location (str): The location where security alert is stored.
        alert_name (str): The unique identifier(uuid) of the security alert
        resource_group_name (Optional[str]): Resource Group Name

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetSecurityAlertResponse]
    """

    return (
        await asyncio_detailed(
            asc_location=asc_location,
            alert_name=alert_name,
            client=client,
            resource_group_name=resource_group_name,
        )
    ).parsed
