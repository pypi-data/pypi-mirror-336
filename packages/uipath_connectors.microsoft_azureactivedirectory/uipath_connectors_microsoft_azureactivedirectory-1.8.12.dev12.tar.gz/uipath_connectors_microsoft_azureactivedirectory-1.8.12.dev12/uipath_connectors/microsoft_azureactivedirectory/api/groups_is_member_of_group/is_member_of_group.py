from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.is_member_of_group_response import IsMemberOfGroupResponse


def _get_kwargs(
    id: str,
    *,
    member_id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["memberId"] = member_id

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/groups/{id}/isMemberOfGroup".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, IsMemberOfGroupResponse]]:
    if response.status_code == 200:
        response_200 = IsMemberOfGroupResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, IsMemberOfGroupResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    member_id: str,
) -> Response[Union[DefaultError, IsMemberOfGroupResponse]]:
    """Is Member of Group

     Verifies if a specific object belongs to a group.

    Args:
        id (str): The Object Id of the group.
        member_id (str): The Object Id of the object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, IsMemberOfGroupResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        member_id=member_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    member_id: str,
) -> Optional[Union[DefaultError, IsMemberOfGroupResponse]]:
    """Is Member of Group

     Verifies if a specific object belongs to a group.

    Args:
        id (str): The Object Id of the group.
        member_id (str): The Object Id of the object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, IsMemberOfGroupResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        member_id=member_id,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    member_id: str,
) -> Response[Union[DefaultError, IsMemberOfGroupResponse]]:
    """Is Member of Group

     Verifies if a specific object belongs to a group.

    Args:
        id (str): The Object Id of the group.
        member_id (str): The Object Id of the object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, IsMemberOfGroupResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        member_id=member_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    member_id: str,
) -> Optional[Union[DefaultError, IsMemberOfGroupResponse]]:
    """Is Member of Group

     Verifies if a specific object belongs to a group.

    Args:
        id (str): The Object Id of the group.
        member_id (str): The Object Id of the object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, IsMemberOfGroupResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            member_id=member_id,
        )
    ).parsed
