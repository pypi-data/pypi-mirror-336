from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.list_calendar_event import ListCalendarEvent
import datetime


def _get_kwargs(
    *,
    timezone: Optional[str] = "UTC",
    from_: datetime.datetime,
    simple_search: Optional[str] = None,
    until: datetime.datetime,
    calendar: Optional[str] = None,
    limit: Optional[str] = "50",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["Timezone"] = timezone

    json_from_ = from_.isoformat()
    params["From"] = json_from_

    params["simpleSearch"] = simple_search

    json_until = until.isoformat()
    params["Until"] = json_until

    params["Calendar"] = calendar

    params["Limit"] = limit

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/hubs/general/ListCalendarEvents",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["ListCalendarEvent"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListCalendarEvent.from_dict(response_200_item_data)

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
) -> Response[Union[DefaultError, list["ListCalendarEvent"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    timezone: Optional[str] = "UTC",
    timezone_lookup: Any,
    from_: datetime.datetime,
    simple_search: Optional[str] = None,
    until: datetime.datetime,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    limit: Optional[str] = "50",
) -> Response[Union[DefaultError, list["ListCalendarEvent"]]]:
    """Get Event List

     Lists events according to filter criteria.

    Args:
        timezone (Optional[str]): Timezone for current event Default: 'UTC'.
        from_ (datetime.datetime): Indicates the date and time as of when to search for events
        simple_search (Optional[str]): The filter is applied to following fields: Summary,
            Description, Attendee's, Display Name, Attendee's Email, and Location.
        until (datetime.datetime): Indicates the date and time until which to search for events
        calendar (Optional[str]): The Calendar for the event. If left empty, default calendar will
            be used.
        limit (Optional[str]): The maximum number of events to return Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListCalendarEvent']]]
    """

    if not timezone and timezone_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/timezones"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if timezone_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for timezone_lookup in timezones")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for timezone_lookup in timezones. Using the first match."
            )

        timezone = found_items[0]["alias"]
    if not calendar and calendar_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/hubs/general/CuratedCalendarList"
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

    kwargs = _get_kwargs(
        timezone=timezone,
        from_=from_,
        simple_search=simple_search,
        until=until,
        calendar=calendar,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    timezone: Optional[str] = "UTC",
    timezone_lookup: Any,
    from_: datetime.datetime,
    simple_search: Optional[str] = None,
    until: datetime.datetime,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    limit: Optional[str] = "50",
) -> Optional[Union[DefaultError, list["ListCalendarEvent"]]]:
    """Get Event List

     Lists events according to filter criteria.

    Args:
        timezone (Optional[str]): Timezone for current event Default: 'UTC'.
        from_ (datetime.datetime): Indicates the date and time as of when to search for events
        simple_search (Optional[str]): The filter is applied to following fields: Summary,
            Description, Attendee's, Display Name, Attendee's Email, and Location.
        until (datetime.datetime): Indicates the date and time until which to search for events
        calendar (Optional[str]): The Calendar for the event. If left empty, default calendar will
            be used.
        limit (Optional[str]): The maximum number of events to return Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListCalendarEvent']]
    """

    return sync_detailed(
        client=client,
        timezone=timezone,
        timezone_lookup=timezone_lookup,
        from_=from_,
        simple_search=simple_search,
        until=until,
        calendar=calendar,
        calendar_lookup=calendar_lookup,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    timezone: Optional[str] = "UTC",
    timezone_lookup: Any,
    from_: datetime.datetime,
    simple_search: Optional[str] = None,
    until: datetime.datetime,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    limit: Optional[str] = "50",
) -> Response[Union[DefaultError, list["ListCalendarEvent"]]]:
    """Get Event List

     Lists events according to filter criteria.

    Args:
        timezone (Optional[str]): Timezone for current event Default: 'UTC'.
        from_ (datetime.datetime): Indicates the date and time as of when to search for events
        simple_search (Optional[str]): The filter is applied to following fields: Summary,
            Description, Attendee's, Display Name, Attendee's Email, and Location.
        until (datetime.datetime): Indicates the date and time until which to search for events
        calendar (Optional[str]): The Calendar for the event. If left empty, default calendar will
            be used.
        limit (Optional[str]): The maximum number of events to return Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListCalendarEvent']]]
    """

    if not timezone and timezone_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/timezones"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if timezone_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for timezone_lookup in timezones")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for timezone_lookup in timezones. Using the first match."
            )

        timezone = found_items[0]["alias"]
    if not calendar and calendar_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/hubs/general/CuratedCalendarList"
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

    kwargs = _get_kwargs(
        timezone=timezone,
        from_=from_,
        simple_search=simple_search,
        until=until,
        calendar=calendar,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    timezone: Optional[str] = "UTC",
    timezone_lookup: Any,
    from_: datetime.datetime,
    simple_search: Optional[str] = None,
    until: datetime.datetime,
    calendar: Optional[str] = None,
    calendar_lookup: Any,
    limit: Optional[str] = "50",
) -> Optional[Union[DefaultError, list["ListCalendarEvent"]]]:
    """Get Event List

     Lists events according to filter criteria.

    Args:
        timezone (Optional[str]): Timezone for current event Default: 'UTC'.
        from_ (datetime.datetime): Indicates the date and time as of when to search for events
        simple_search (Optional[str]): The filter is applied to following fields: Summary,
            Description, Attendee's, Display Name, Attendee's Email, and Location.
        until (datetime.datetime): Indicates the date and time until which to search for events
        calendar (Optional[str]): The Calendar for the event. If left empty, default calendar will
            be used.
        limit (Optional[str]): The maximum number of events to return Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListCalendarEvent']]
    """

    return (
        await asyncio_detailed(
            client=client,
            timezone=timezone,
            timezone_lookup=timezone_lookup,
            from_=from_,
            simple_search=simple_search,
            until=until,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            limit=limit,
        )
    ).parsed
