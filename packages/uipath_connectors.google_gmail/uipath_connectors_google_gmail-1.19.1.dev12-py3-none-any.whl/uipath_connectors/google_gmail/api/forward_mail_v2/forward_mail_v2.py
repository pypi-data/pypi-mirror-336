from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.forward_mail_v2_body import ForwardMailV2Body
from ...models.forward_mail_v2_response import ForwardMailV2Response


def _get_kwargs(
    *,
    body: ForwardMailV2Body,
    id: str,
    save_as_draft: Optional[bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["id"] = id

    params["saveAsDraft"] = save_as_draft

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/ForwardMailV2",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, ForwardMailV2Response]]:
    if response.status_code == 200:
        response_200 = ForwardMailV2Response.from_dict(response.json())

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
) -> Response[Union[DefaultError, ForwardMailV2Response]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ForwardMailV2Body,
    id: str,
    save_as_draft: Optional[bool] = False,
) -> Response[Union[DefaultError, ForwardMailV2Response]]:
    """Forward Email

     Forwards an email in Gmail to another recipient

    Args:
        id (str): The ID of email to forward
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent Default: False.
        body (ForwardMailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, ForwardMailV2Response]]
    """

    kwargs = _get_kwargs(
        body=body,
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
    body: ForwardMailV2Body,
    id: str,
    save_as_draft: Optional[bool] = False,
) -> Optional[Union[DefaultError, ForwardMailV2Response]]:
    """Forward Email

     Forwards an email in Gmail to another recipient

    Args:
        id (str): The ID of email to forward
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent Default: False.
        body (ForwardMailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, ForwardMailV2Response]
    """

    return sync_detailed(
        client=client,
        body=body,
        id=id,
        save_as_draft=save_as_draft,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ForwardMailV2Body,
    id: str,
    save_as_draft: Optional[bool] = False,
) -> Response[Union[DefaultError, ForwardMailV2Response]]:
    """Forward Email

     Forwards an email in Gmail to another recipient

    Args:
        id (str): The ID of email to forward
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent Default: False.
        body (ForwardMailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, ForwardMailV2Response]]
    """

    kwargs = _get_kwargs(
        body=body,
        id=id,
        save_as_draft=save_as_draft,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ForwardMailV2Body,
    id: str,
    save_as_draft: Optional[bool] = False,
) -> Optional[Union[DefaultError, ForwardMailV2Response]]:
    """Forward Email

     Forwards an email in Gmail to another recipient

    Args:
        id (str): The ID of email to forward
        save_as_draft (Optional[bool]): Specifies whether the email should be saved as draft
            instead of being sent Default: False.
        body (ForwardMailV2Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, ForwardMailV2Response]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            id=id,
            save_as_draft=save_as_draft,
        )
    ).parsed
