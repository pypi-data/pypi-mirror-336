from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_folder_content import GetFolderContent


def _get_kwargs(
    *,
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    include_deleted: Optional[bool] = None,
    include_mounted_folders: Optional[bool] = None,
    include_has_explicit_shared_members: Optional[bool] = None,
    recursive: Optional[bool] = None,
    include_non_downloadable_files: Optional[bool] = None,
    folder_path: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["pageSize"] = page_size

    params["nextPage"] = next_page

    params["include_deleted"] = include_deleted

    params["include_mounted_folders"] = include_mounted_folders

    params["include_has_explicit_shared_members"] = include_has_explicit_shared_members

    params["recursive"] = recursive

    params["include_non_downloadable_files"] = include_non_downloadable_files

    params["folderPath"] = folder_path

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/get_folder_contents",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["GetFolderContent"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetFolderContent.from_dict(response_200_item_data)

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
) -> Response[Union[DefaultError, list["GetFolderContent"]]]:
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
    include_deleted: Optional[bool] = None,
    include_mounted_folders: Optional[bool] = None,
    include_has_explicit_shared_members: Optional[bool] = None,
    recursive: Optional[bool] = None,
    include_non_downloadable_files: Optional[bool] = None,
    folder_path: Optional[str] = None,
    folder_path_lookup: Any,
) -> Response[Union[DefaultError, list["GetFolderContent"]]]:
    """Get Folder Items

     Lists items in a selected folder in Dropbox

    Args:
        page_size (Optional[int]): The page size for pagination, which defaults to 200 if not
            supplied
        next_page (Optional[str]): The next page cursor, taken from the response header: elements-
            next-page-token
        include_deleted (Optional[bool]): If true, the results will include entries for files and
            folders that used to exist but were deleted. The default for this field is False.
        include_mounted_folders (Optional[bool]):  If true, the results will include entries under
            mounted folders which includes app folder, shared folder and team folder. The default for
            this field is True.
        include_has_explicit_shared_members (Optional[bool]):  If true, the results will include a
            flag for each file indicating whether or not that file has any explicit members. The
            default for this field is False.
        recursive (Optional[bool]): If true, the list folder operation will be applied recursively
            to all subfolders and the response will contain contents of all subfolders. The default
            for this field is False.
        include_non_downloadable_files (Optional[bool]):  If true, include files that are not
            downloadable, i.e. Google Docs. The default for this field is True.
        folder_path (Optional[str]): The folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetFolderContent']]]
    """

    if not folder_path and folder_path_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/curated_folders"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if folder_path_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for folder_path_lookup in curated_folders"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for folder_path_lookup in curated_folders. Using the first match."
            )

        folder_path = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        page_size=page_size,
        next_page=next_page,
        include_deleted=include_deleted,
        include_mounted_folders=include_mounted_folders,
        include_has_explicit_shared_members=include_has_explicit_shared_members,
        recursive=recursive,
        include_non_downloadable_files=include_non_downloadable_files,
        folder_path=folder_path,
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
    include_deleted: Optional[bool] = None,
    include_mounted_folders: Optional[bool] = None,
    include_has_explicit_shared_members: Optional[bool] = None,
    recursive: Optional[bool] = None,
    include_non_downloadable_files: Optional[bool] = None,
    folder_path: Optional[str] = None,
    folder_path_lookup: Any,
) -> Optional[Union[DefaultError, list["GetFolderContent"]]]:
    """Get Folder Items

     Lists items in a selected folder in Dropbox

    Args:
        page_size (Optional[int]): The page size for pagination, which defaults to 200 if not
            supplied
        next_page (Optional[str]): The next page cursor, taken from the response header: elements-
            next-page-token
        include_deleted (Optional[bool]): If true, the results will include entries for files and
            folders that used to exist but were deleted. The default for this field is False.
        include_mounted_folders (Optional[bool]):  If true, the results will include entries under
            mounted folders which includes app folder, shared folder and team folder. The default for
            this field is True.
        include_has_explicit_shared_members (Optional[bool]):  If true, the results will include a
            flag for each file indicating whether or not that file has any explicit members. The
            default for this field is False.
        recursive (Optional[bool]): If true, the list folder operation will be applied recursively
            to all subfolders and the response will contain contents of all subfolders. The default
            for this field is False.
        include_non_downloadable_files (Optional[bool]):  If true, include files that are not
            downloadable, i.e. Google Docs. The default for this field is True.
        folder_path (Optional[str]): The folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetFolderContent']]
    """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_page=next_page,
        include_deleted=include_deleted,
        include_mounted_folders=include_mounted_folders,
        include_has_explicit_shared_members=include_has_explicit_shared_members,
        recursive=recursive,
        include_non_downloadable_files=include_non_downloadable_files,
        folder_path=folder_path,
        folder_path_lookup=folder_path_lookup,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    include_deleted: Optional[bool] = None,
    include_mounted_folders: Optional[bool] = None,
    include_has_explicit_shared_members: Optional[bool] = None,
    recursive: Optional[bool] = None,
    include_non_downloadable_files: Optional[bool] = None,
    folder_path: Optional[str] = None,
    folder_path_lookup: Any,
) -> Response[Union[DefaultError, list["GetFolderContent"]]]:
    """Get Folder Items

     Lists items in a selected folder in Dropbox

    Args:
        page_size (Optional[int]): The page size for pagination, which defaults to 200 if not
            supplied
        next_page (Optional[str]): The next page cursor, taken from the response header: elements-
            next-page-token
        include_deleted (Optional[bool]): If true, the results will include entries for files and
            folders that used to exist but were deleted. The default for this field is False.
        include_mounted_folders (Optional[bool]):  If true, the results will include entries under
            mounted folders which includes app folder, shared folder and team folder. The default for
            this field is True.
        include_has_explicit_shared_members (Optional[bool]):  If true, the results will include a
            flag for each file indicating whether or not that file has any explicit members. The
            default for this field is False.
        recursive (Optional[bool]): If true, the list folder operation will be applied recursively
            to all subfolders and the response will contain contents of all subfolders. The default
            for this field is False.
        include_non_downloadable_files (Optional[bool]):  If true, include files that are not
            downloadable, i.e. Google Docs. The default for this field is True.
        folder_path (Optional[str]): The folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetFolderContent']]]
    """

    if not folder_path and folder_path_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/curated_folders"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if folder_path_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for folder_path_lookup in curated_folders"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for folder_path_lookup in curated_folders. Using the first match."
            )

        folder_path = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        page_size=page_size,
        next_page=next_page,
        include_deleted=include_deleted,
        include_mounted_folders=include_mounted_folders,
        include_has_explicit_shared_members=include_has_explicit_shared_members,
        recursive=recursive,
        include_non_downloadable_files=include_non_downloadable_files,
        folder_path=folder_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    include_deleted: Optional[bool] = None,
    include_mounted_folders: Optional[bool] = None,
    include_has_explicit_shared_members: Optional[bool] = None,
    recursive: Optional[bool] = None,
    include_non_downloadable_files: Optional[bool] = None,
    folder_path: Optional[str] = None,
    folder_path_lookup: Any,
) -> Optional[Union[DefaultError, list["GetFolderContent"]]]:
    """Get Folder Items

     Lists items in a selected folder in Dropbox

    Args:
        page_size (Optional[int]): The page size for pagination, which defaults to 200 if not
            supplied
        next_page (Optional[str]): The next page cursor, taken from the response header: elements-
            next-page-token
        include_deleted (Optional[bool]): If true, the results will include entries for files and
            folders that used to exist but were deleted. The default for this field is False.
        include_mounted_folders (Optional[bool]):  If true, the results will include entries under
            mounted folders which includes app folder, shared folder and team folder. The default for
            this field is True.
        include_has_explicit_shared_members (Optional[bool]):  If true, the results will include a
            flag for each file indicating whether or not that file has any explicit members. The
            default for this field is False.
        recursive (Optional[bool]): If true, the list folder operation will be applied recursively
            to all subfolders and the response will contain contents of all subfolders. The default
            for this field is False.
        include_non_downloadable_files (Optional[bool]):  If true, include files that are not
            downloadable, i.e. Google Docs. The default for this field is True.
        folder_path (Optional[str]): The folder path

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetFolderContent']]
    """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_page=next_page,
            include_deleted=include_deleted,
            include_mounted_folders=include_mounted_folders,
            include_has_explicit_shared_members=include_has_explicit_shared_members,
            recursive=recursive,
            include_non_downloadable_files=include_non_downloadable_files,
            folder_path=folder_path,
            folder_path_lookup=folder_path_lookup,
        )
    ).parsed
