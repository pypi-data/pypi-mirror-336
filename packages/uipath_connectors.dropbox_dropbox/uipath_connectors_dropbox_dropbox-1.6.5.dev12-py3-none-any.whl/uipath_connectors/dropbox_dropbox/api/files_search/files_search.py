from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.files_search import FilesSearch


def _get_kwargs(
    *,
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    file_extensions: Optional[str] = None,
    include_highlights: Optional[bool] = None,
    file_categories: Optional[str] = None,
    account_id: Optional[str] = None,
    filename_only: Optional[bool] = None,
    order_by: Optional[str] = None,
    file_status: Optional[str] = None,
    query: str,
    file_extensions_items: Optional[str] = None,
    path: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["pageSize"] = page_size

    params["nextPage"] = next_page

    params["file_extensions"] = file_extensions

    params["include_highlights"] = include_highlights

    params["file_categories"] = file_categories

    params["account_id"] = account_id

    params["filename_only"] = filename_only

    params["order_by"] = order_by

    params["file_status"] = file_status

    params["query"] = query

    params["file_extensions[*]"] = file_extensions_items

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/files_search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["FilesSearch"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FilesSearch.from_dict(response_200_item_data)

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
) -> Response[Union[DefaultError, list["FilesSearch"]]]:
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
    file_extensions: Optional[str] = None,
    include_highlights: Optional[bool] = None,
    file_categories: Optional[str] = None,
    account_id: Optional[str] = None,
    filename_only: Optional[bool] = None,
    order_by: Optional[str] = None,
    file_status: Optional[str] = None,
    query: str,
    file_extensions_items: Optional[str] = None,
    path: Optional[str] = None,
    path_lookup: Any,
) -> Response[Union[DefaultError, list["FilesSearch"]]]:
    """Search Files

     Searches for files and folders

    Args:
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The page number of resources to retrieve
        file_extensions (Optional[str]): File extensions
        include_highlights (Optional[bool]): Include highlights
        file_categories (Optional[str]): Category of file to search for.  These are static and set
            by Dropbox.
        account_id (Optional[str]): The owner of the file
        filename_only (Optional[bool]): File name Only
        order_by (Optional[str]): Order by
        file_status (Optional[str]): The status of file being sought
        query (str): The search query to return files and folders. Please check vendor
            documentation for help.
        file_extensions_items (Optional[str]): The file type or extension to search for.  Add the
            extension and press enter to add multiple.
        path (Optional[str]): The File or Folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['FilesSearch']]]
    """

    if not path and path_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/curated_folders"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if path_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for path_lookup in curated_folders")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for path_lookup in curated_folders. Using the first match."
            )

        path = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        page_size=page_size,
        next_page=next_page,
        file_extensions=file_extensions,
        include_highlights=include_highlights,
        file_categories=file_categories,
        account_id=account_id,
        filename_only=filename_only,
        order_by=order_by,
        file_status=file_status,
        query=query,
        file_extensions_items=file_extensions_items,
        path=path,
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
    file_extensions: Optional[str] = None,
    include_highlights: Optional[bool] = None,
    file_categories: Optional[str] = None,
    account_id: Optional[str] = None,
    filename_only: Optional[bool] = None,
    order_by: Optional[str] = None,
    file_status: Optional[str] = None,
    query: str,
    file_extensions_items: Optional[str] = None,
    path: Optional[str] = None,
    path_lookup: Any,
) -> Optional[Union[DefaultError, list["FilesSearch"]]]:
    """Search Files

     Searches for files and folders

    Args:
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The page number of resources to retrieve
        file_extensions (Optional[str]): File extensions
        include_highlights (Optional[bool]): Include highlights
        file_categories (Optional[str]): Category of file to search for.  These are static and set
            by Dropbox.
        account_id (Optional[str]): The owner of the file
        filename_only (Optional[bool]): File name Only
        order_by (Optional[str]): Order by
        file_status (Optional[str]): The status of file being sought
        query (str): The search query to return files and folders. Please check vendor
            documentation for help.
        file_extensions_items (Optional[str]): The file type or extension to search for.  Add the
            extension and press enter to add multiple.
        path (Optional[str]): The File or Folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['FilesSearch']]
    """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_page=next_page,
        file_extensions=file_extensions,
        include_highlights=include_highlights,
        file_categories=file_categories,
        account_id=account_id,
        filename_only=filename_only,
        order_by=order_by,
        file_status=file_status,
        query=query,
        file_extensions_items=file_extensions_items,
        path=path,
        path_lookup=path_lookup,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    file_extensions: Optional[str] = None,
    include_highlights: Optional[bool] = None,
    file_categories: Optional[str] = None,
    account_id: Optional[str] = None,
    filename_only: Optional[bool] = None,
    order_by: Optional[str] = None,
    file_status: Optional[str] = None,
    query: str,
    file_extensions_items: Optional[str] = None,
    path: Optional[str] = None,
    path_lookup: Any,
) -> Response[Union[DefaultError, list["FilesSearch"]]]:
    """Search Files

     Searches for files and folders

    Args:
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The page number of resources to retrieve
        file_extensions (Optional[str]): File extensions
        include_highlights (Optional[bool]): Include highlights
        file_categories (Optional[str]): Category of file to search for.  These are static and set
            by Dropbox.
        account_id (Optional[str]): The owner of the file
        filename_only (Optional[bool]): File name Only
        order_by (Optional[str]): Order by
        file_status (Optional[str]): The status of file being sought
        query (str): The search query to return files and folders. Please check vendor
            documentation for help.
        file_extensions_items (Optional[str]): The file type or extension to search for.  Add the
            extension and press enter to add multiple.
        path (Optional[str]): The File or Folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['FilesSearch']]]
    """

    if not path and path_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/curated_folders"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if path_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for path_lookup in curated_folders")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for path_lookup in curated_folders. Using the first match."
            )

        path = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        page_size=page_size,
        next_page=next_page,
        file_extensions=file_extensions,
        include_highlights=include_highlights,
        file_categories=file_categories,
        account_id=account_id,
        filename_only=filename_only,
        order_by=order_by,
        file_status=file_status,
        query=query,
        file_extensions_items=file_extensions_items,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    file_extensions: Optional[str] = None,
    include_highlights: Optional[bool] = None,
    file_categories: Optional[str] = None,
    account_id: Optional[str] = None,
    filename_only: Optional[bool] = None,
    order_by: Optional[str] = None,
    file_status: Optional[str] = None,
    query: str,
    file_extensions_items: Optional[str] = None,
    path: Optional[str] = None,
    path_lookup: Any,
) -> Optional[Union[DefaultError, list["FilesSearch"]]]:
    """Search Files

     Searches for files and folders

    Args:
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The page number of resources to retrieve
        file_extensions (Optional[str]): File extensions
        include_highlights (Optional[bool]): Include highlights
        file_categories (Optional[str]): Category of file to search for.  These are static and set
            by Dropbox.
        account_id (Optional[str]): The owner of the file
        filename_only (Optional[bool]): File name Only
        order_by (Optional[str]): Order by
        file_status (Optional[str]): The status of file being sought
        query (str): The search query to return files and folders. Please check vendor
            documentation for help.
        file_extensions_items (Optional[str]): The file type or extension to search for.  Add the
            extension and press enter to add multiple.
        path (Optional[str]): The File or Folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['FilesSearch']]
    """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_page=next_page,
            file_extensions=file_extensions,
            include_highlights=include_highlights,
            file_categories=file_categories,
            account_id=account_id,
            filename_only=filename_only,
            order_by=order_by,
            file_status=file_status,
            query=query,
            file_extensions_items=file_extensions_items,
            path=path,
            path_lookup=path_lookup,
        )
    ).parsed
