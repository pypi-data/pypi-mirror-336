from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_file_info_response import GetFileInfoResponse


def _get_kwargs(
    files_id: str,
    *,
    x_rep_hints: Optional[str] = None,
    elements_vendor_headers: Optional[str] = None,
    if_none_match: Optional[str] = None,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if elements_vendor_headers is not None:
        headers["elements-vendor-headers"] = elements_vendor_headers

    if if_none_match is not None:
        headers["if-none-match"] = if_none_match

    params: dict[str, Any] = {}

    params["x-rep-hints"] = x_rep_hints

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/files/{files_id}".format(
            files_id=files_id,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, GetFileInfoResponse]]:
    if response.status_code == 200:
        response_200 = GetFileInfoResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, GetFileInfoResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    files_id_lookup: Any,
    files_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_rep_hints: Optional[str] = None,
    elements_vendor_headers: Optional[str] = None,
    if_none_match: Optional[str] = None,
) -> Response[Union[DefaultError, GetFileInfoResponse]]:
    """Get File Info

      Gets the full file object for a given file

    Args:
        files_id (str): The files id
        x_rep_hints (Optional[str]): A header required to request specific representations of a
            file. Use this in combination with the fields query parameter to request a specific file
            representation. Ex: pdf
        elements_vendor_headers (Optional[str]): The URL, and optional password, for the shared
            link of this item.This header can be used to access items that have not been explicitly
            shared with a user. Ex: shared_link=[link]&shared_link_password=[password]. ***Value
            passed under the header elements-vendor-headers will be mapped to “boxapi” header in this
            case.
        if_none_match (Optional[str]): Ensures an item is only returned if it has changed. Ex: 1

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetFileInfoResponse]]
    """

    if not files_id and files_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/folder_picker_folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if files_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for files_id_lookup in folder_picker_folder"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for files_id_lookup in folder_picker_folder. Using the first match."
            )

        files_id = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        files_id=files_id,
        x_rep_hints=x_rep_hints,
        elements_vendor_headers=elements_vendor_headers,
        if_none_match=if_none_match,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    files_id_lookup: Any,
    files_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_rep_hints: Optional[str] = None,
    elements_vendor_headers: Optional[str] = None,
    if_none_match: Optional[str] = None,
) -> Optional[Union[DefaultError, GetFileInfoResponse]]:
    """Get File Info

      Gets the full file object for a given file

    Args:
        files_id (str): The files id
        x_rep_hints (Optional[str]): A header required to request specific representations of a
            file. Use this in combination with the fields query parameter to request a specific file
            representation. Ex: pdf
        elements_vendor_headers (Optional[str]): The URL, and optional password, for the shared
            link of this item.This header can be used to access items that have not been explicitly
            shared with a user. Ex: shared_link=[link]&shared_link_password=[password]. ***Value
            passed under the header elements-vendor-headers will be mapped to “boxapi” header in this
            case.
        if_none_match (Optional[str]): Ensures an item is only returned if it has changed. Ex: 1

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetFileInfoResponse]
    """

    return sync_detailed(
        files_id=files_id,
        files_id_lookup=files_id_lookup,
        client=client,
        x_rep_hints=x_rep_hints,
        elements_vendor_headers=elements_vendor_headers,
        if_none_match=if_none_match,
    ).parsed


async def asyncio_detailed(
    files_id_lookup: Any,
    files_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_rep_hints: Optional[str] = None,
    elements_vendor_headers: Optional[str] = None,
    if_none_match: Optional[str] = None,
) -> Response[Union[DefaultError, GetFileInfoResponse]]:
    """Get File Info

      Gets the full file object for a given file

    Args:
        files_id (str): The files id
        x_rep_hints (Optional[str]): A header required to request specific representations of a
            file. Use this in combination with the fields query parameter to request a specific file
            representation. Ex: pdf
        elements_vendor_headers (Optional[str]): The URL, and optional password, for the shared
            link of this item.This header can be used to access items that have not been explicitly
            shared with a user. Ex: shared_link=[link]&shared_link_password=[password]. ***Value
            passed under the header elements-vendor-headers will be mapped to “boxapi” header in this
            case.
        if_none_match (Optional[str]): Ensures an item is only returned if it has changed. Ex: 1

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, GetFileInfoResponse]]
    """

    if not files_id and files_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/folder_picker_folder"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if files_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for files_id_lookup in folder_picker_folder"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for files_id_lookup in folder_picker_folder. Using the first match."
            )

        files_id = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        files_id=files_id,
        x_rep_hints=x_rep_hints,
        elements_vendor_headers=elements_vendor_headers,
        if_none_match=if_none_match,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    files_id_lookup: Any,
    files_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    x_rep_hints: Optional[str] = None,
    elements_vendor_headers: Optional[str] = None,
    if_none_match: Optional[str] = None,
) -> Optional[Union[DefaultError, GetFileInfoResponse]]:
    """Get File Info

      Gets the full file object for a given file

    Args:
        files_id (str): The files id
        x_rep_hints (Optional[str]): A header required to request specific representations of a
            file. Use this in combination with the fields query parameter to request a specific file
            representation. Ex: pdf
        elements_vendor_headers (Optional[str]): The URL, and optional password, for the shared
            link of this item.This header can be used to access items that have not been explicitly
            shared with a user. Ex: shared_link=[link]&shared_link_password=[password]. ***Value
            passed under the header elements-vendor-headers will be mapped to “boxapi” header in this
            case.
        if_none_match (Optional[str]): Ensures an item is only returned if it has changed. Ex: 1

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, GetFileInfoResponse]
    """

    return (
        await asyncio_detailed(
            files_id=files_id,
            files_id_lookup=files_id_lookup,
            client=client,
            x_rep_hints=x_rep_hints,
            elements_vendor_headers=elements_vendor_headers,
            if_none_match=if_none_match,
        )
    ).parsed
