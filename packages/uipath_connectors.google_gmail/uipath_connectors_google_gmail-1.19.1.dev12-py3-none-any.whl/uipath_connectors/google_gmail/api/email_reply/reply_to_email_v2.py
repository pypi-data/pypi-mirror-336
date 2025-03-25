from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.reply_to_email_v2_body import ReplyToEmailV2Body
from ...models.reply_to_email_v2_response import ReplyToEmailV2Response


def _get_kwargs(
    *,
    body: ReplyToEmailV2Body,
    reply_to_all: Optional[bool] = False,
    id: str,
    save_as_draft: Optional[bool] = None,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["replyToAll"] = reply_to_all

    params["id"] = id

    params["saveAsDraft"] = save_as_draft

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/EmailReply",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, ReplyToEmailV2Response]]:
    if response.status_code == 200:
        response_200 = ReplyToEmailV2Response.from_dict(response.json())

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
) -> Response[Union[DefaultError, ReplyToEmailV2Response]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ReplyToEmailV2Body,
    reply_to_all: Optional[bool] = False,
    id: str,
    save_as_draft: Optional[bool] = None,
) -> Response[Union[DefaultError, ReplyToEmailV2Response]]:
    """Reply to Email

     Sends a reply to an email based on email ID

    Args:
        reply_to_all (Optional[bool]): Specifies whether to send the reply to all the recipients
            of the initial email Default: False.
        id (str): The ID of email to reply to. This can be retrieved from a trigger activity or
            get email activities.
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent
        body (ReplyToEmailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, ReplyToEmailV2Response]]
    """

    kwargs = _get_kwargs(
        body=body,
        reply_to_all=reply_to_all,
        id=id,
        save_as_draft=save_as_draft,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ReplyToEmailV2Body,
    reply_to_all: Optional[bool] = False,
    id: str,
    save_as_draft: Optional[bool] = None,
) -> Optional[Union[DefaultError, ReplyToEmailV2Response]]:
    """Reply to Email

     Sends a reply to an email based on email ID

    Args:
        reply_to_all (Optional[bool]): Specifies whether to send the reply to all the recipients
            of the initial email Default: False.
        id (str): The ID of email to reply to. This can be retrieved from a trigger activity or
            get email activities.
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent
        body (ReplyToEmailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, ReplyToEmailV2Response]
    """

    return sync_detailed(
        client=client,
        body=body,
        reply_to_all=reply_to_all,
        id=id,
        save_as_draft=save_as_draft,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ReplyToEmailV2Body,
    reply_to_all: Optional[bool] = False,
    id: str,
    save_as_draft: Optional[bool] = None,
) -> Response[Union[DefaultError, ReplyToEmailV2Response]]:
    """Reply to Email

     Sends a reply to an email based on email ID

    Args:
        reply_to_all (Optional[bool]): Specifies whether to send the reply to all the recipients
            of the initial email Default: False.
        id (str): The ID of email to reply to. This can be retrieved from a trigger activity or
            get email activities.
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent
        body (ReplyToEmailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, ReplyToEmailV2Response]]
    """

    kwargs = _get_kwargs(
        body=body,
        reply_to_all=reply_to_all,
        id=id,
        save_as_draft=save_as_draft,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ReplyToEmailV2Body,
    reply_to_all: Optional[bool] = False,
    id: str,
    save_as_draft: Optional[bool] = None,
) -> Optional[Union[DefaultError, ReplyToEmailV2Response]]:
    """Reply to Email

     Sends a reply to an email based on email ID

    Args:
        reply_to_all (Optional[bool]): Specifies whether to send the reply to all the recipients
            of the initial email Default: False.
        id (str): The ID of email to reply to. This can be retrieved from a trigger activity or
            get email activities.
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent
        body (ReplyToEmailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, ReplyToEmailV2Response]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            reply_to_all=reply_to_all,
            id=id,
            save_as_draft=save_as_draft,
        )
    ).parsed
