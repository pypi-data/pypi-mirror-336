from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.mark_email_read_unread_response import MarkEmailReadUnreadResponse


def _get_kwargs(
    *,
    id: str,
    mark_as: Optional[str] = "read",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["id"] = id

    params["markAs"] = mark_as

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/MarkEmailReadUnread",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, MarkEmailReadUnreadResponse]]:
    if response.status_code == 200:
        response_200 = MarkEmailReadUnreadResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, MarkEmailReadUnreadResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
    mark_as: Optional[str] = "read",
) -> Response[Union[DefaultError, MarkEmailReadUnreadResponse]]:
    """Mark Email as Read or UnRead

     Mark Email as Read or UnRead

    Args:
        id (str): The ID of email to mark read or unread.
        mark_as (Optional[str]): The new state of the selected email Default: 'read'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, MarkEmailReadUnreadResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        mark_as=mark_as,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
    mark_as: Optional[str] = "read",
) -> Optional[Union[DefaultError, MarkEmailReadUnreadResponse]]:
    """Mark Email as Read or UnRead

     Mark Email as Read or UnRead

    Args:
        id (str): The ID of email to mark read or unread.
        mark_as (Optional[str]): The new state of the selected email Default: 'read'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, MarkEmailReadUnreadResponse]
    """

    return sync_detailed(
        client=client,
        id=id,
        mark_as=mark_as,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
    mark_as: Optional[str] = "read",
) -> Response[Union[DefaultError, MarkEmailReadUnreadResponse]]:
    """Mark Email as Read or UnRead

     Mark Email as Read or UnRead

    Args:
        id (str): The ID of email to mark read or unread.
        mark_as (Optional[str]): The new state of the selected email Default: 'read'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, MarkEmailReadUnreadResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        mark_as=mark_as,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
    mark_as: Optional[str] = "read",
) -> Optional[Union[DefaultError, MarkEmailReadUnreadResponse]]:
    """Mark Email as Read or UnRead

     Mark Email as Read or UnRead

    Args:
        id (str): The ID of email to mark read or unread.
        mark_as (Optional[str]): The new state of the selected email Default: 'read'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, MarkEmailReadUnreadResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            mark_as=mark_as,
        )
    ).parsed
