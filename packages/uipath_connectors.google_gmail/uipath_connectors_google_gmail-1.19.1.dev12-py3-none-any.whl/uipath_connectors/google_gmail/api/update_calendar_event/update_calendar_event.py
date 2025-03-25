from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.update_calendar_event_request import UpdateCalendarEventRequest
from ...models.update_calendar_event_response import UpdateCalendarEventResponse


def _get_kwargs(
    id: str,
    *,
    body: UpdateCalendarEventRequest,
    calendar: Optional[str] = None,
    output_timezone: Optional[str] = None,
    add_conference_data: Optional[bool] = None,
    send_notifications: Optional[str] = "All",
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["Calendar"] = calendar

    params["outputTimezone"] = output_timezone

    params["AddConferenceData"] = add_conference_data

    params["SendNotifications"] = send_notifications

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/hubs/general/UpdateCalendarEvents/{id}".format(
            id=id,
        ),
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, UpdateCalendarEventResponse]]:
    if response.status_code == 200:
        response_200 = UpdateCalendarEventResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, UpdateCalendarEventResponse]]:
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
    body: UpdateCalendarEventRequest,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    add_conference_data: Optional[bool] = None,
    send_notifications: Optional[str] = "All",
) -> Response[Union[DefaultError, UpdateCalendarEventResponse]]:
    """Update Event (Calendar Event)

     Updates an event in calendar

    Args:
        id (str): The event to update
        calendar (Optional[str]): Calendar for event.
        output_timezone (Optional[str]): Timezone for output event
        add_conference_data (Optional[bool]): If adding conference data is allowed or not.
        send_notifications (Optional[str]): Whether to send notifications about the creation of
            the new event. Note that some emails might still be sent. The default is false.

            Valid values: all, externalOnly, none Default: 'All'.
        body (UpdateCalendarEventRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateCalendarEventResponse]]
    """

    if not calendar and calendar_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/CuratedCalendarList"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if calendar_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for calendar_lookup in CuratedCalendarList"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for calendar_lookup in CuratedCalendarList. Using the first match."
            )

        calendar = found_items[0]["ID"]
    if not output_timezone and output_timezone_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/timezones"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if output_timezone_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for output_timezone_lookup in timezones"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for output_timezone_lookup in timezones. Using the first match."
            )

        output_timezone = found_items[0]["alias"]

    kwargs = _get_kwargs(
        id=id,
        body=body,
        calendar=calendar,
        output_timezone=output_timezone,
        add_conference_data=add_conference_data,
        send_notifications=send_notifications,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateCalendarEventRequest,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    add_conference_data: Optional[bool] = None,
    send_notifications: Optional[str] = "All",
) -> Optional[Union[DefaultError, UpdateCalendarEventResponse]]:
    """Update Event (Calendar Event)

     Updates an event in calendar

    Args:
        id (str): The event to update
        calendar (Optional[str]): Calendar for event.
        output_timezone (Optional[str]): Timezone for output event
        add_conference_data (Optional[bool]): If adding conference data is allowed or not.
        send_notifications (Optional[str]): Whether to send notifications about the creation of
            the new event. Note that some emails might still be sent. The default is false.

            Valid values: all, externalOnly, none Default: 'All'.
        body (UpdateCalendarEventRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateCalendarEventResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        calendar=calendar,
        calendar_lookup=calendar_lookup,
        output_timezone=output_timezone,
        output_timezone_lookup=output_timezone_lookup,
        add_conference_data=add_conference_data,
        send_notifications=send_notifications,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateCalendarEventRequest,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    add_conference_data: Optional[bool] = None,
    send_notifications: Optional[str] = "All",
) -> Response[Union[DefaultError, UpdateCalendarEventResponse]]:
    """Update Event (Calendar Event)

     Updates an event in calendar

    Args:
        id (str): The event to update
        calendar (Optional[str]): Calendar for event.
        output_timezone (Optional[str]): Timezone for output event
        add_conference_data (Optional[bool]): If adding conference data is allowed or not.
        send_notifications (Optional[str]): Whether to send notifications about the creation of
            the new event. Note that some emails might still be sent. The default is false.

            Valid values: all, externalOnly, none Default: 'All'.
        body (UpdateCalendarEventRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateCalendarEventResponse]]
    """

    if not calendar and calendar_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/CuratedCalendarList"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if calendar_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for calendar_lookup in CuratedCalendarList"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for calendar_lookup in CuratedCalendarList. Using the first match."
            )

        calendar = found_items[0]["ID"]
    if not output_timezone and output_timezone_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/timezones"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if output_timezone_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for output_timezone_lookup in timezones"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for output_timezone_lookup in timezones. Using the first match."
            )

        output_timezone = found_items[0]["alias"]

    kwargs = _get_kwargs(
        id=id,
        body=body,
        calendar=calendar,
        output_timezone=output_timezone,
        add_conference_data=add_conference_data,
        send_notifications=send_notifications,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateCalendarEventRequest,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    add_conference_data: Optional[bool] = None,
    send_notifications: Optional[str] = "All",
) -> Optional[Union[DefaultError, UpdateCalendarEventResponse]]:
    """Update Event (Calendar Event)

     Updates an event in calendar

    Args:
        id (str): The event to update
        calendar (Optional[str]): Calendar for event.
        output_timezone (Optional[str]): Timezone for output event
        add_conference_data (Optional[bool]): If adding conference data is allowed or not.
        send_notifications (Optional[str]): Whether to send notifications about the creation of
            the new event. Note that some emails might still be sent. The default is false.

            Valid values: all, externalOnly, none Default: 'All'.
        body (UpdateCalendarEventRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateCalendarEventResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            output_timezone=output_timezone,
            output_timezone_lookup=output_timezone_lookup,
            add_conference_data=add_conference_data,
            send_notifications=send_notifications,
        )
    ).parsed
