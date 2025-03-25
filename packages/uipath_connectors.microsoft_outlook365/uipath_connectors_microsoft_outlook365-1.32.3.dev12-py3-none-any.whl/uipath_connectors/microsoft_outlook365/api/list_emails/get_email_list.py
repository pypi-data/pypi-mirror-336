from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_email_list import GetEmailList


def _get_kwargs(
    *,
    un_read_only: Optional[bool] = False,
    filter_: Optional[str] = None,
    limit: Optional[str] = "100",
    importance: Optional[str] = None,
    parent_folder_id: str,
    with_attachments_only: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    mark_as_read: Optional[bool] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["unReadOnly"] = un_read_only

    params["filter"] = filter_

    params["limit"] = limit

    params["importance"] = importance

    params["parentFolderId"] = parent_folder_id

    params["withAttachmentsOnly"] = with_attachments_only

    params["includeSubfolders"] = include_subfolders

    params["markAsRead"] = mark_as_read

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ListEmails",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["GetEmailList"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetEmailList.from_dict(response_200_item_data)

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
) -> Response[Union[DefaultError, list["GetEmailList"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    un_read_only: Optional[bool] = False,
    filter_: Optional[str] = None,
    limit: Optional[str] = "100",
    importance: Optional[str] = None,
    parent_folder_id: str,
    parent_folder_id_lookup: Any,
    with_attachments_only: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    mark_as_read: Optional[bool] = None,
) -> Response[Union[DefaultError, list["GetEmailList"]]]:
    """Get Email List

     Get list of emails from selected folder from outlook

    Args:
        un_read_only (Optional[bool]): Indicates whether to consider only unread emails or not
            Default: False.
        filter_ (Optional[str]): Additional OData filters
        limit (Optional[str]): The number of emails to retrieve Default: '100'.
        importance (Optional[str]): Importance of the email
        parent_folder_id (str): The folder to get the emails from
        with_attachments_only (Optional[bool]): Indicates whether to consider only emails with
            attachments or not Default: False.
        include_subfolders (Optional[bool]): Indicates whether to expand the search to include all
            subfolders of the selected mail folder or not Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieved email as read

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetEmailList']]]
    """

    if not parent_folder_id and parent_folder_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/MailFolders"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if parent_folder_id_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for parent_folder_id_lookup in MailFolder"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for parent_folder_id_lookup in MailFolder. Using the first match."
            )

        parent_folder_id = found_items[0]["id"]

    kwargs = _get_kwargs(
        un_read_only=un_read_only,
        filter_=filter_,
        limit=limit,
        importance=importance,
        parent_folder_id=parent_folder_id,
        with_attachments_only=with_attachments_only,
        include_subfolders=include_subfolders,
        mark_as_read=mark_as_read,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    un_read_only: Optional[bool] = False,
    filter_: Optional[str] = None,
    limit: Optional[str] = "100",
    importance: Optional[str] = None,
    parent_folder_id: str,
    parent_folder_id_lookup: Any,
    with_attachments_only: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    mark_as_read: Optional[bool] = None,
) -> Optional[Union[DefaultError, list["GetEmailList"]]]:
    """Get Email List

     Get list of emails from selected folder from outlook

    Args:
        un_read_only (Optional[bool]): Indicates whether to consider only unread emails or not
            Default: False.
        filter_ (Optional[str]): Additional OData filters
        limit (Optional[str]): The number of emails to retrieve Default: '100'.
        importance (Optional[str]): Importance of the email
        parent_folder_id (str): The folder to get the emails from
        with_attachments_only (Optional[bool]): Indicates whether to consider only emails with
            attachments or not Default: False.
        include_subfolders (Optional[bool]): Indicates whether to expand the search to include all
            subfolders of the selected mail folder or not Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieved email as read

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetEmailList']]
    """

    return sync_detailed(
        client=client,
        un_read_only=un_read_only,
        filter_=filter_,
        limit=limit,
        importance=importance,
        parent_folder_id=parent_folder_id,
        parent_folder_id_lookup=parent_folder_id_lookup,
        with_attachments_only=with_attachments_only,
        include_subfolders=include_subfolders,
        mark_as_read=mark_as_read,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    un_read_only: Optional[bool] = False,
    filter_: Optional[str] = None,
    limit: Optional[str] = "100",
    importance: Optional[str] = None,
    parent_folder_id: str,
    parent_folder_id_lookup: Any,
    with_attachments_only: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    mark_as_read: Optional[bool] = None,
) -> Response[Union[DefaultError, list["GetEmailList"]]]:
    """Get Email List

     Get list of emails from selected folder from outlook

    Args:
        un_read_only (Optional[bool]): Indicates whether to consider only unread emails or not
            Default: False.
        filter_ (Optional[str]): Additional OData filters
        limit (Optional[str]): The number of emails to retrieve Default: '100'.
        importance (Optional[str]): Importance of the email
        parent_folder_id (str): The folder to get the emails from
        with_attachments_only (Optional[bool]): Indicates whether to consider only emails with
            attachments or not Default: False.
        include_subfolders (Optional[bool]): Indicates whether to expand the search to include all
            subfolders of the selected mail folder or not Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieved email as read

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetEmailList']]]
    """

    if not parent_folder_id and parent_folder_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/MailFolders"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if parent_folder_id_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for parent_folder_id_lookup in MailFolder"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for parent_folder_id_lookup in MailFolder. Using the first match."
            )

        parent_folder_id = found_items[0]["id"]

    kwargs = _get_kwargs(
        un_read_only=un_read_only,
        filter_=filter_,
        limit=limit,
        importance=importance,
        parent_folder_id=parent_folder_id,
        with_attachments_only=with_attachments_only,
        include_subfolders=include_subfolders,
        mark_as_read=mark_as_read,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    un_read_only: Optional[bool] = False,
    filter_: Optional[str] = None,
    limit: Optional[str] = "100",
    importance: Optional[str] = None,
    parent_folder_id: str,
    parent_folder_id_lookup: Any,
    with_attachments_only: Optional[bool] = False,
    include_subfolders: Optional[bool] = False,
    mark_as_read: Optional[bool] = None,
) -> Optional[Union[DefaultError, list["GetEmailList"]]]:
    """Get Email List

     Get list of emails from selected folder from outlook

    Args:
        un_read_only (Optional[bool]): Indicates whether to consider only unread emails or not
            Default: False.
        filter_ (Optional[str]): Additional OData filters
        limit (Optional[str]): The number of emails to retrieve Default: '100'.
        importance (Optional[str]): Importance of the email
        parent_folder_id (str): The folder to get the emails from
        with_attachments_only (Optional[bool]): Indicates whether to consider only emails with
            attachments or not Default: False.
        include_subfolders (Optional[bool]): Indicates whether to expand the search to include all
            subfolders of the selected mail folder or not Default: False.
        mark_as_read (Optional[bool]): Indicates whether to mark the retrieved email as read

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetEmailList']]
    """

    return (
        await asyncio_detailed(
            client=client,
            un_read_only=un_read_only,
            filter_=filter_,
            limit=limit,
            importance=importance,
            parent_folder_id=parent_folder_id,
            parent_folder_id_lookup=parent_folder_id_lookup,
            with_attachments_only=with_attachments_only,
            include_subfolders=include_subfolders,
            mark_as_read=mark_as_read,
        )
    ).parsed
