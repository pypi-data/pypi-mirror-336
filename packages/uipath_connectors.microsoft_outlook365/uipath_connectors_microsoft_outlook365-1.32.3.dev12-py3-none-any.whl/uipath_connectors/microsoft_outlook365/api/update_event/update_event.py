from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.update_event_body import UpdateEventBody
from ...models.update_event_response import UpdateEventResponse


def _get_kwargs(
    id: str,
    *,
    body: UpdateEventBody,
    calendar_id: Optional[str] = None,
    output_timezone: Optional[str] = None,
    remove_attachment_id: Optional[str] = None,
    change_attachment: Optional[str] = None,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["calendarID"] = calendar_id

    params["outputTimezone"] = output_timezone

    params["removeAttachmentID"] = remove_attachment_id

    params["changeAttachment"] = change_attachment

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/UpdateEvent/{id}".format(
            id=id,
        ),
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, UpdateEventResponse]]:
    if response.status_code == 200:
        response_200 = UpdateEventResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, UpdateEventResponse]]:
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
    body: UpdateEventBody,
    calendar_id: Optional[str] = None,
    calendar_id_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    remove_attachment_id: Optional[str] = None,
    change_attachment: Optional[str] = None,
) -> Response[Union[DefaultError, UpdateEventResponse]]:
    """Update Event (Calendar Event)

    Args:
        id (str): The ID of event to modify
        calendar_id (Optional[str]): The ID of calendar in which respective event is present
        output_timezone (Optional[str]): Timezone for output event
        remove_attachment_id (Optional[str]): The ID of attachment to be removed from event
        change_attachment (Optional[str]): Change attachment associated with event
        body (UpdateEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateEventResponse]]
    """

    if not calendar_id and calendar_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/CalendarList"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if calendar_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for calendar_id_lookup in CalendarList")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for calendar_id_lookup in CalendarList. Using the first match."
            )

        calendar_id = found_items[0]["ID"]
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
        calendar_id=calendar_id,
        output_timezone=output_timezone,
        remove_attachment_id=remove_attachment_id,
        change_attachment=change_attachment,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateEventBody,
    calendar_id: Optional[str] = None,
    calendar_id_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    remove_attachment_id: Optional[str] = None,
    change_attachment: Optional[str] = None,
) -> Optional[Union[DefaultError, UpdateEventResponse]]:
    """Update Event (Calendar Event)

    Args:
        id (str): The ID of event to modify
        calendar_id (Optional[str]): The ID of calendar in which respective event is present
        output_timezone (Optional[str]): Timezone for output event
        remove_attachment_id (Optional[str]): The ID of attachment to be removed from event
        change_attachment (Optional[str]): Change attachment associated with event
        body (UpdateEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateEventResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        calendar_id=calendar_id,
        calendar_id_lookup=calendar_id_lookup,
        output_timezone=output_timezone,
        output_timezone_lookup=output_timezone_lookup,
        remove_attachment_id=remove_attachment_id,
        change_attachment=change_attachment,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateEventBody,
    calendar_id: Optional[str] = None,
    calendar_id_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    remove_attachment_id: Optional[str] = None,
    change_attachment: Optional[str] = None,
) -> Response[Union[DefaultError, UpdateEventResponse]]:
    """Update Event (Calendar Event)

    Args:
        id (str): The ID of event to modify
        calendar_id (Optional[str]): The ID of calendar in which respective event is present
        output_timezone (Optional[str]): Timezone for output event
        remove_attachment_id (Optional[str]): The ID of attachment to be removed from event
        change_attachment (Optional[str]): Change attachment associated with event
        body (UpdateEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateEventResponse]]
    """

    if not calendar_id and calendar_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/CalendarList"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if calendar_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for calendar_id_lookup in CalendarList")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for calendar_id_lookup in CalendarList. Using the first match."
            )

        calendar_id = found_items[0]["ID"]
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
        calendar_id=calendar_id,
        output_timezone=output_timezone,
        remove_attachment_id=remove_attachment_id,
        change_attachment=change_attachment,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateEventBody,
    calendar_id: Optional[str] = None,
    calendar_id_lookup: Any,
    output_timezone: Optional[str] = None,
    output_timezone_lookup: Any,
    remove_attachment_id: Optional[str] = None,
    change_attachment: Optional[str] = None,
) -> Optional[Union[DefaultError, UpdateEventResponse]]:
    """Update Event (Calendar Event)

    Args:
        id (str): The ID of event to modify
        calendar_id (Optional[str]): The ID of calendar in which respective event is present
        output_timezone (Optional[str]): Timezone for output event
        remove_attachment_id (Optional[str]): The ID of attachment to be removed from event
        change_attachment (Optional[str]): Change attachment associated with event
        body (UpdateEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateEventResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
            output_timezone=output_timezone,
            output_timezone_lookup=output_timezone_lookup,
            remove_attachment_id=remove_attachment_id,
            change_attachment=change_attachment,
        )
    ).parsed
