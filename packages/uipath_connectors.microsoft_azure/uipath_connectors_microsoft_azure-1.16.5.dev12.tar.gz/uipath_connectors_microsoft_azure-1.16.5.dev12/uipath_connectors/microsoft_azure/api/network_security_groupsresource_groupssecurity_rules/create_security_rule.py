from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.create_security_rule_request import CreateSecurityRuleRequest
from ...models.create_security_rule_response import CreateSecurityRuleResponse
from ...models.default_error import DefaultError


def _get_kwargs(
    network_security_group: str,
    resource_group_name: str,
    network_security_rule: str,
    *,
    body: CreateSecurityRuleRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/networkSecurityGroups/{network_security_group}/resourceGroups/{resource_group_name}/securityRules/{network_security_rule}".format(
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateSecurityRuleResponse, DefaultError]]:
    if response.status_code == 200:
        response_200 = CreateSecurityRuleResponse.from_dict(response.json())

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
) -> Response[Union[CreateSecurityRuleResponse, DefaultError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    network_security_group: str,
    resource_group_name: str,
    network_security_rule: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSecurityRuleRequest,
) -> Response[Union[CreateSecurityRuleResponse, DefaultError]]:
    """Create Security Rule

     Creates or updates a security rule in a specified network security group.

    Args:
        network_security_group (str): The name of the network security group to which the rule
            belongs
        resource_group_name (str): The name of the Resource Group.
        network_security_rule (str): The name of the security rule.
        body (CreateSecurityRuleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSecurityRuleResponse, DefaultError]]
    """

    kwargs = _get_kwargs(
        network_security_group=network_security_group,
        resource_group_name=resource_group_name,
        network_security_rule=network_security_rule,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    network_security_group: str,
    resource_group_name: str,
    network_security_rule: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSecurityRuleRequest,
) -> Optional[Union[CreateSecurityRuleResponse, DefaultError]]:
    """Create Security Rule

     Creates or updates a security rule in a specified network security group.

    Args:
        network_security_group (str): The name of the network security group to which the rule
            belongs
        resource_group_name (str): The name of the Resource Group.
        network_security_rule (str): The name of the security rule.
        body (CreateSecurityRuleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSecurityRuleResponse, DefaultError]
    """

    return sync_detailed(
        network_security_group=network_security_group,
        resource_group_name=resource_group_name,
        network_security_rule=network_security_rule,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    network_security_group: str,
    resource_group_name: str,
    network_security_rule: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSecurityRuleRequest,
) -> Response[Union[CreateSecurityRuleResponse, DefaultError]]:
    """Create Security Rule

     Creates or updates a security rule in a specified network security group.

    Args:
        network_security_group (str): The name of the network security group to which the rule
            belongs
        resource_group_name (str): The name of the Resource Group.
        network_security_rule (str): The name of the security rule.
        body (CreateSecurityRuleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSecurityRuleResponse, DefaultError]]
    """

    kwargs = _get_kwargs(
        network_security_group=network_security_group,
        resource_group_name=resource_group_name,
        network_security_rule=network_security_rule,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    network_security_group: str,
    resource_group_name: str,
    network_security_rule: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSecurityRuleRequest,
) -> Optional[Union[CreateSecurityRuleResponse, DefaultError]]:
    """Create Security Rule

     Creates or updates a security rule in a specified network security group.

    Args:
        network_security_group (str): The name of the network security group to which the rule
            belongs
        resource_group_name (str): The name of the Resource Group.
        network_security_rule (str): The name of the security rule.
        body (CreateSecurityRuleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSecurityRuleResponse, DefaultError]
    """

    return (
        await asyncio_detailed(
            network_security_group=network_security_group,
            resource_group_name=resource_group_name,
            network_security_rule=network_security_rule,
            client=client,
            body=body,
        )
    ).parsed
