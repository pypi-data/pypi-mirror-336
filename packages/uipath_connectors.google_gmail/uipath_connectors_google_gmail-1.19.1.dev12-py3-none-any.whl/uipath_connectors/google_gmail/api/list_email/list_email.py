from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.list_email import ListEmail


def _get_kwargs(
    *,
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    with_attachments_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    starred_only: Optional[bool] = False,
    limit_emails_to_first: Optional[str] = "50",
    email_folder: str,
    unread_only: Optional[bool] = False,
    additional_filters: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["pageSize"] = page_size

    params["nextPage"] = next_page

    params["withAttachmentsOnly"] = with_attachments_only

    params["importantOnly"] = important_only

    params["markAsRead"] = mark_as_read

    params["includeSubfolders"] = include_subfolders

    params["starredOnly"] = starred_only

    params["limitEmailsToFirst"] = limit_emails_to_first

    params["emailFolder"] = email_folder

    params["unreadOnly"] = unread_only

    params["additionalFilters"] = additional_filters

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/hubs/general/ListEmails",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListEmail.from_dict(response_200_item_data)

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
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    with_attachments_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    starred_only: Optional[bool] = False,
    limit_emails_to_first: Optional[str] = "50",
    email_folder: str,
    email_folder_lookup: Any,
    unread_only: Optional[bool] = False,
    additional_filters: str,
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    """Get Email List

     Lists emails according to filter criteria

    Args:
        page_size (Optional[int]): The page size. Max and defaults to 10 if not provided.
        next_page (Optional[str]): The next page cursor, taken from the response header `elements-
            next-page-token`
        with_attachments_only (Optional[bool]): Return emails with only attachment. Default:
            False.
        important_only (Optional[bool]): Return only important emails. Default: False.
        mark_as_read (Optional[bool]): Indicates wether to mark the retrieved mails as read
            Default: False.
        include_subfolders (Optional[bool]): Include email messages from selected folder's
            subfolder Default: False.
        starred_only (Optional[bool]): Return only starred emails. Default: False.
        limit_emails_to_first (Optional[str]): The number of email to retrieve Default: '50'.
        email_folder (str): The folder or label to get email messages from
        unread_only (Optional[bool]): Return only unread emails. Default: False.
        additional_filters (str): Additional filters.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListEmail']]]
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
        page_size=page_size,
        next_page=next_page,
        with_attachments_only=with_attachments_only,
        important_only=important_only,
        mark_as_read=mark_as_read,
        include_subfolders=include_subfolders,
        starred_only=starred_only,
        limit_emails_to_first=limit_emails_to_first,
        email_folder=email_folder,
        unread_only=unread_only,
        additional_filters=additional_filters,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    with_attachments_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    starred_only: Optional[bool] = False,
    limit_emails_to_first: Optional[str] = "50",
    email_folder: str,
    email_folder_lookup: Any,
    unread_only: Optional[bool] = False,
    additional_filters: str,
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    """Get Email List

     Lists emails according to filter criteria

    Args:
        page_size (Optional[int]): The page size. Max and defaults to 10 if not provided.
        next_page (Optional[str]): The next page cursor, taken from the response header `elements-
            next-page-token`
        with_attachments_only (Optional[bool]): Return emails with only attachment. Default:
            False.
        important_only (Optional[bool]): Return only important emails. Default: False.
        mark_as_read (Optional[bool]): Indicates wether to mark the retrieved mails as read
            Default: False.
        include_subfolders (Optional[bool]): Include email messages from selected folder's
            subfolder Default: False.
        starred_only (Optional[bool]): Return only starred emails. Default: False.
        limit_emails_to_first (Optional[str]): The number of email to retrieve Default: '50'.
        email_folder (str): The folder or label to get email messages from
        unread_only (Optional[bool]): Return only unread emails. Default: False.
        additional_filters (str): Additional filters.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListEmail']]
    """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_page=next_page,
        with_attachments_only=with_attachments_only,
        important_only=important_only,
        mark_as_read=mark_as_read,
        include_subfolders=include_subfolders,
        starred_only=starred_only,
        limit_emails_to_first=limit_emails_to_first,
        email_folder=email_folder,
        email_folder_lookup=email_folder_lookup,
        unread_only=unread_only,
        additional_filters=additional_filters,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    with_attachments_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    starred_only: Optional[bool] = False,
    limit_emails_to_first: Optional[str] = "50",
    email_folder: str,
    email_folder_lookup: Any,
    unread_only: Optional[bool] = False,
    additional_filters: str,
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    """Get Email List

     Lists emails according to filter criteria

    Args:
        page_size (Optional[int]): The page size. Max and defaults to 10 if not provided.
        next_page (Optional[str]): The next page cursor, taken from the response header `elements-
            next-page-token`
        with_attachments_only (Optional[bool]): Return emails with only attachment. Default:
            False.
        important_only (Optional[bool]): Return only important emails. Default: False.
        mark_as_read (Optional[bool]): Indicates wether to mark the retrieved mails as read
            Default: False.
        include_subfolders (Optional[bool]): Include email messages from selected folder's
            subfolder Default: False.
        starred_only (Optional[bool]): Return only starred emails. Default: False.
        limit_emails_to_first (Optional[str]): The number of email to retrieve Default: '50'.
        email_folder (str): The folder or label to get email messages from
        unread_only (Optional[bool]): Return only unread emails. Default: False.
        additional_filters (str): Additional filters.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListEmail']]]
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
        page_size=page_size,
        next_page=next_page,
        with_attachments_only=with_attachments_only,
        important_only=important_only,
        mark_as_read=mark_as_read,
        include_subfolders=include_subfolders,
        starred_only=starred_only,
        limit_emails_to_first=limit_emails_to_first,
        email_folder=email_folder,
        unread_only=unread_only,
        additional_filters=additional_filters,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    with_attachments_only: Optional[bool] = False,
    important_only: Optional[bool] = False,
    mark_as_read: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    starred_only: Optional[bool] = False,
    limit_emails_to_first: Optional[str] = "50",
    email_folder: str,
    email_folder_lookup: Any,
    unread_only: Optional[bool] = False,
    additional_filters: str,
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    """Get Email List

     Lists emails according to filter criteria

    Args:
        page_size (Optional[int]): The page size. Max and defaults to 10 if not provided.
        next_page (Optional[str]): The next page cursor, taken from the response header `elements-
            next-page-token`
        with_attachments_only (Optional[bool]): Return emails with only attachment. Default:
            False.
        important_only (Optional[bool]): Return only important emails. Default: False.
        mark_as_read (Optional[bool]): Indicates wether to mark the retrieved mails as read
            Default: False.
        include_subfolders (Optional[bool]): Include email messages from selected folder's
            subfolder Default: False.
        starred_only (Optional[bool]): Return only starred emails. Default: False.
        limit_emails_to_first (Optional[str]): The number of email to retrieve Default: '50'.
        email_folder (str): The folder or label to get email messages from
        unread_only (Optional[bool]): Return only unread emails. Default: False.
        additional_filters (str): Additional filters.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListEmail']]
    """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_page=next_page,
            with_attachments_only=with_attachments_only,
            important_only=important_only,
            mark_as_read=mark_as_read,
            include_subfolders=include_subfolders,
            starred_only=starred_only,
            limit_emails_to_first=limit_emails_to_first,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            unread_only=unread_only,
            additional_filters=additional_filters,
        )
    ).parsed
