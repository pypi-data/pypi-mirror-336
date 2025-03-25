from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_newest_email_response import GetNewestEmailResponse


def _get_kwargs(
    *,
    unread_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    email_folder: str,
    additional_filter: Optional[str] = None,
    with_attachment_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    starred_only: Optional[bool] = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["unreadOnly"] = unread_only

    params["importantOnly"] = important_only

    params["emailFolder"] = email_folder

    params["additionalFilter"] = additional_filter

    params["withAttachmentOnly"] = with_attachment_only

    params["markAsRead"] = mark_as_read

    params["starredOnly"] = starred_only

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/GetNewestEmail",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, GetNewestEmailResponse]]:
    if response.status_code == 200:
        response_200 = GetNewestEmailResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, GetNewestEmailResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    unread_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    email_folder: str,
    email_folder_lookup: Any,
    additional_filter: Optional[str] = None,
    with_attachment_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    starred_only: Optional[bool] = False,
) -> Response[Union[DefaultError, GetNewestEmailResponse]]:
    """Get Newest Email

     Fetch newest email from the list of emails in specified folder

    Args:
        unread_only (Optional[bool]): Indicate whether to include only unread emails Default:
            False.
        important_only (Optional[bool]): Indicates whether to consider only important emails
            Default: False.
        email_folder (str): The folder or label from where to get email messages
        additional_filter (Optional[str]): Additional filter for query
        with_attachment_only (Optional[bool]): Indicates whether to include only emails with
            attachment Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieve email as read
            Default: False.
        starred_only (Optional[bool]): Indicates whether to consider only starred emails Default:
            False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetNewestEmailResponse]]
    """

    if not email_folder and email_folder_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if email_folder_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for email_folder_lookup in folder")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for email_folder_lookup in folder. Using the first match."
            )

        email_folder = found_items[0]["referenceID"]

    kwargs = _get_kwargs(
        unread_only=unread_only,
        important_only=important_only,
        email_folder=email_folder,
        additional_filter=additional_filter,
        with_attachment_only=with_attachment_only,
        mark_as_read=mark_as_read,
        starred_only=starred_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    unread_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    email_folder: str,
    email_folder_lookup: Any,
    additional_filter: Optional[str] = None,
    with_attachment_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    starred_only: Optional[bool] = False,
) -> Optional[Union[DefaultError, GetNewestEmailResponse]]:
    """Get Newest Email

     Fetch newest email from the list of emails in specified folder

    Args:
        unread_only (Optional[bool]): Indicate whether to include only unread emails Default:
            False.
        important_only (Optional[bool]): Indicates whether to consider only important emails
            Default: False.
        email_folder (str): The folder or label from where to get email messages
        additional_filter (Optional[str]): Additional filter for query
        with_attachment_only (Optional[bool]): Indicates whether to include only emails with
            attachment Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieve email as read
            Default: False.
        starred_only (Optional[bool]): Indicates whether to consider only starred emails Default:
            False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetNewestEmailResponse]
    """

    return sync_detailed(
        client=client,
        unread_only=unread_only,
        important_only=important_only,
        email_folder=email_folder,
        email_folder_lookup=email_folder_lookup,
        additional_filter=additional_filter,
        with_attachment_only=with_attachment_only,
        mark_as_read=mark_as_read,
        starred_only=starred_only,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    unread_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    email_folder: str,
    email_folder_lookup: Any,
    additional_filter: Optional[str] = None,
    with_attachment_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    starred_only: Optional[bool] = False,
) -> Response[Union[DefaultError, GetNewestEmailResponse]]:
    """Get Newest Email

     Fetch newest email from the list of emails in specified folder

    Args:
        unread_only (Optional[bool]): Indicate whether to include only unread emails Default:
            False.
        important_only (Optional[bool]): Indicates whether to consider only important emails
            Default: False.
        email_folder (str): The folder or label from where to get email messages
        additional_filter (Optional[str]): Additional filter for query
        with_attachment_only (Optional[bool]): Indicates whether to include only emails with
            attachment Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieve email as read
            Default: False.
        starred_only (Optional[bool]): Indicates whether to consider only starred emails Default:
            False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetNewestEmailResponse]]
    """

    if not email_folder and email_folder_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if email_folder_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for email_folder_lookup in folder")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for email_folder_lookup in folder. Using the first match."
            )

        email_folder = found_items[0]["referenceID"]

    kwargs = _get_kwargs(
        unread_only=unread_only,
        important_only=important_only,
        email_folder=email_folder,
        additional_filter=additional_filter,
        with_attachment_only=with_attachment_only,
        mark_as_read=mark_as_read,
        starred_only=starred_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    unread_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    email_folder: str,
    email_folder_lookup: Any,
    additional_filter: Optional[str] = None,
    with_attachment_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    starred_only: Optional[bool] = False,
) -> Optional[Union[DefaultError, GetNewestEmailResponse]]:
    """Get Newest Email

     Fetch newest email from the list of emails in specified folder

    Args:
        unread_only (Optional[bool]): Indicate whether to include only unread emails Default:
            False.
        important_only (Optional[bool]): Indicates whether to consider only important emails
            Default: False.
        email_folder (str): The folder or label from where to get email messages
        additional_filter (Optional[str]): Additional filter for query
        with_attachment_only (Optional[bool]): Indicates whether to include only emails with
            attachment Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieve email as read
            Default: False.
        starred_only (Optional[bool]): Indicates whether to consider only starred emails Default:
            False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetNewestEmailResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            unread_only=unread_only,
            important_only=important_only,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            additional_filter=additional_filter,
            with_attachment_only=with_attachment_only,
            mark_as_read=mark_as_read,
            starred_only=starred_only,
        )
    ).parsed
