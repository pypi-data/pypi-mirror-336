from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.move_email_response import MoveEmailResponse


def _get_kwargs(
    *,
    add_label_id: str,
    id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["addLabelId"] = add_label_id

    params["id"] = id

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/MoveEmail",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, MoveEmailResponse]]:
    if response.status_code == 200:
        response_200 = MoveEmailResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, MoveEmailResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    add_label_id: str,
    add_label_id_lookup: Any,
    id: str,
) -> Response[Union[DefaultError, MoveEmailResponse]]:
    """Move Email

     Move an email in Gmail to a folder or label

    Args:
        add_label_id (str): The folder or label where to move the email message
        id (str): The email ID to move

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, MoveEmailResponse]]
    """

    if not add_label_id and add_label_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if add_label_id_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for add_label_id_lookup in folder")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for add_label_id_lookup in folder. Using the first match."
            )

        add_label_id = found_items[0]["id"]

    kwargs = _get_kwargs(
        add_label_id=add_label_id,
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    add_label_id: str,
    add_label_id_lookup: Any,
    id: str,
) -> Optional[Union[DefaultError, MoveEmailResponse]]:
    """Move Email

     Move an email in Gmail to a folder or label

    Args:
        add_label_id (str): The folder or label where to move the email message
        id (str): The email ID to move

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, MoveEmailResponse]
    """

    return sync_detailed(
        client=client,
        add_label_id=add_label_id,
        add_label_id_lookup=add_label_id_lookup,
        id=id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    add_label_id: str,
    add_label_id_lookup: Any,
    id: str,
) -> Response[Union[DefaultError, MoveEmailResponse]]:
    """Move Email

     Move an email in Gmail to a folder or label

    Args:
        add_label_id (str): The folder or label where to move the email message
        id (str): The email ID to move

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, MoveEmailResponse]]
    """

    if not add_label_id and add_label_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if add_label_id_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for add_label_id_lookup in folder")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for add_label_id_lookup in folder. Using the first match."
            )

        add_label_id = found_items[0]["id"]

    kwargs = _get_kwargs(
        add_label_id=add_label_id,
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    add_label_id: str,
    add_label_id_lookup: Any,
    id: str,
) -> Optional[Union[DefaultError, MoveEmailResponse]]:
    """Move Email

     Move an email in Gmail to a folder or label

    Args:
        add_label_id (str): The folder or label where to move the email message
        id (str): The email ID to move

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, MoveEmailResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            add_label_id=add_label_id,
            add_label_id_lookup=add_label_id_lookup,
            id=id,
        )
    ).parsed
