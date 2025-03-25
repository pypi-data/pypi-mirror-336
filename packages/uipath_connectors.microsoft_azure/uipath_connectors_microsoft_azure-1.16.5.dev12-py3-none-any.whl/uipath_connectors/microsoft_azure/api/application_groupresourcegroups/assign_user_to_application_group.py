from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.assign_user_to_application_group_response import (
    AssignUserToApplicationGroupResponse,
)
from ...models.default_error import DefaultError


def _get_kwargs(
    application_group_name: str,
    resource_group_name: str,
    *,
    object_id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["objectId"] = object_id

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/applicationGroup/{application_group_name}/resourcegroups/{resource_group_name}".format(
            application_group_name=application_group_name,
            resource_group_name=resource_group_name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
    if response.status_code == 200:
        response_200 = AssignUserToApplicationGroupResponse.from_dict(response.json())

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
) -> Response[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    application_group_name: str,
    resource_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    object_id: str,
) -> Response[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
    """Assign User to Application Group

     Assign User To Application Group

    Args:
        application_group_name (str): The application group name
        resource_group_name (str): The resource group name
        object_id (str): The object Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssignUserToApplicationGroupResponse, DefaultError]]
    """

    kwargs = _get_kwargs(
        application_group_name=application_group_name,
        resource_group_name=resource_group_name,
        object_id=object_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    application_group_name: str,
    resource_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    object_id: str,
) -> Optional[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
    """Assign User to Application Group

     Assign User To Application Group

    Args:
        application_group_name (str): The application group name
        resource_group_name (str): The resource group name
        object_id (str): The object Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssignUserToApplicationGroupResponse, DefaultError]
    """

    return sync_detailed(
        application_group_name=application_group_name,
        resource_group_name=resource_group_name,
        client=client,
        object_id=object_id,
    ).parsed


async def asyncio_detailed(
    application_group_name: str,
    resource_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    object_id: str,
) -> Response[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
    """Assign User to Application Group

     Assign User To Application Group

    Args:
        application_group_name (str): The application group name
        resource_group_name (str): The resource group name
        object_id (str): The object Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssignUserToApplicationGroupResponse, DefaultError]]
    """

    kwargs = _get_kwargs(
        application_group_name=application_group_name,
        resource_group_name=resource_group_name,
        object_id=object_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_group_name: str,
    resource_group_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    object_id: str,
) -> Optional[Union[AssignUserToApplicationGroupResponse, DefaultError]]:
    """Assign User to Application Group

     Assign User To Application Group

    Args:
        application_group_name (str): The application group name
        resource_group_name (str): The resource group name
        object_id (str): The object Id

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssignUserToApplicationGroupResponse, DefaultError]
    """

    return (
        await asyncio_detailed(
            application_group_name=application_group_name,
            resource_group_name=resource_group_name,
            client=client,
            object_id=object_id,
        )
    ).parsed
