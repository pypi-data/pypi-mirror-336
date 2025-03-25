from .members import (
    delete_members as _delete_members,
    delete_members_async as _delete_members_async,
    list_members as _list_members,
    list_members_async as _list_members_async,
    get_member as _get_member,
    get_member_async as _get_member_async,
)
from ..models.default_error import DefaultError
from typing import cast
from ..models.list_members import ListMembers
from ..models.get_member_response import GetMemberResponse
from .add_team_members import (
    add_members as _add_members,
    add_members_async as _add_members_async,
)
from ..models.add_members_request import AddMembersRequest
from ..models.add_members_response import AddMembersResponse
from .files_copy import (
    copy_files as _copy_files,
    copy_files_async as _copy_files_async,
)
from ..models.copy_files_request import CopyFilesRequest
from ..models.copy_files_response import CopyFilesResponse
from .folders_copy import (
    copy_folder as _copy_folder,
    copy_folder_async as _copy_folder_async,
)
from ..models.copy_folder_request import CopyFolderRequest
from ..models.copy_folder_response import CopyFolderResponse
from .create_folder import (
    create_folders as _create_folders,
    create_folders_async as _create_folders_async,
)
from ..models.create_folders_request import CreateFoldersRequest
from ..models.create_folders_response import CreateFoldersResponse
from .create_shared_links import (
    create_shared_links as _create_shared_links,
    create_shared_links_async as _create_shared_links_async,
)
from ..models.create_shared_links_request import CreateSharedLinksRequest
from ..models.create_shared_links_response import CreateSharedLinksResponse
from .delete_file import (
    delete_file as _delete_file,
    delete_file_async as _delete_file_async,
)
from .delete_folder import (
    delete_folders as _delete_folders,
    delete_folders_async as _delete_folders_async,
)
from .files_download import (
    file_downloads as _file_downloads,
    file_downloads_async as _file_downloads_async,
)
from ..models.file_downloads_response import FileDownloadsResponse
from ..types import File
from io import BytesIO
from .upload_file import (
    file_uploads as _file_uploads,
    file_uploads_async as _file_uploads_async,
)
from ..models.file_uploads_body import FileUploadsBody
from ..models.file_uploads_request import FileUploadsRequest
from ..models.file_uploads_response import FileUploadsResponse
from .files_search import (
    files_search as _files_search,
    files_search_async as _files_search_async,
)
from ..models.files_search import FilesSearch
from .get_file_details import (
    get_file_details as _get_file_details,
    get_file_details_async as _get_file_details_async,
)
from ..models.get_file_details_response import GetFileDetailsResponse
from .get_folder_contents import (
    get_folder_content as _get_folder_content,
    get_folder_content_async as _get_folder_content_async,
)
from ..models.get_folder_content import GetFolderContent
from .get_shared_links import (
    get_shared_link as _get_shared_link,
    get_shared_link_async as _get_shared_link_async,
)
from ..models.get_shared_link_response import GetSharedLinkResponse
from .suspend_members import (
    suspend_members as _suspend_members,
    suspend_members_async as _suspend_members_async,
)
from .unsuspend_members import (
    unsuspendmembers as _unsuspendmembers,
    unsuspendmembers_async as _unsuspendmembers_async,
)

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class DropboxDropbox:
    def __init__(self, *, instance_id: str, client: httpx.Client):
        base_url = str(client.base_url).rstrip("/")
        new_headers = {
            k: v for k, v in client.headers.items() if k not in ["content-type"]
        }
        new_client = httpx.Client(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        new_client_async = httpx.AsyncClient(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        self.client = (
            Client(
                base_url="",  # this will be overridden by the base_url in the Client constructor
            )
            .set_httpx_client(new_client)
            .set_async_httpx_client(new_client_async)
        )

    def delete_members(
        self,
        id_lookup: Any,
        id: str,
        *,
        wipe_data: Optional[bool] = None,
        keep_account: Optional[bool] = None,
        transfer_admin_id: Optional[str] = None,
        transfer_dest_id: Optional[str] = None,
        retain_team_shares: Optional[bool] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_members(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
            wipe_data=wipe_data,
            keep_account=keep_account,
            transfer_admin_id=transfer_admin_id,
            transfer_dest_id=transfer_dest_id,
            retain_team_shares=retain_team_shares,
        )

    async def delete_members_async(
        self,
        id_lookup: Any,
        id: str,
        *,
        wipe_data: Optional[bool] = None,
        keep_account: Optional[bool] = None,
        transfer_admin_id: Optional[str] = None,
        transfer_dest_id: Optional[str] = None,
        retain_team_shares: Optional[bool] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_members_async(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
            wipe_data=wipe_data,
            keep_account=keep_account,
            transfer_admin_id=transfer_admin_id,
            transfer_dest_id=transfer_dest_id,
            retain_team_shares=retain_team_shares,
        )

    def list_members(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        include_removed: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListMembers"]]]:
        return _list_members(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            include_removed=include_removed,
        )

    async def list_members_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        include_removed: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["ListMembers"]]]:
        return await _list_members_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            include_removed=include_removed,
        )

    def get_member(
        self,
        id_lookup: Any,
        id: str,
    ) -> Optional[Union[DefaultError, GetMemberResponse]]:
        return _get_member(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    async def get_member_async(
        self,
        id_lookup: Any,
        id: str,
    ) -> Optional[Union[DefaultError, GetMemberResponse]]:
        return await _get_member_async(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    def add_members(
        self,
        *,
        body: AddMembersRequest,
    ) -> Optional[Union[AddMembersResponse, DefaultError]]:
        return _add_members(
            client=self.client,
            body=body,
        )

    async def add_members_async(
        self,
        *,
        body: AddMembersRequest,
    ) -> Optional[Union[AddMembersResponse, DefaultError]]:
        return await _add_members_async(
            client=self.client,
            body=body,
        )

    def copy_files(
        self,
        *,
        body: CopyFilesRequest,
    ) -> Optional[Union[CopyFilesResponse, DefaultError]]:
        return _copy_files(
            client=self.client,
            body=body,
        )

    async def copy_files_async(
        self,
        *,
        body: CopyFilesRequest,
    ) -> Optional[Union[CopyFilesResponse, DefaultError]]:
        return await _copy_files_async(
            client=self.client,
            body=body,
        )

    def copy_folder(
        self,
        *,
        body: CopyFolderRequest,
    ) -> Optional[Union[CopyFolderResponse, DefaultError]]:
        return _copy_folder(
            client=self.client,
            body=body,
        )

    async def copy_folder_async(
        self,
        *,
        body: CopyFolderRequest,
    ) -> Optional[Union[CopyFolderResponse, DefaultError]]:
        return await _copy_folder_async(
            client=self.client,
            body=body,
        )

    def create_folders(
        self,
        *,
        body: CreateFoldersRequest,
    ) -> Optional[Union[CreateFoldersResponse, DefaultError]]:
        return _create_folders(
            client=self.client,
            body=body,
        )

    async def create_folders_async(
        self,
        *,
        body: CreateFoldersRequest,
    ) -> Optional[Union[CreateFoldersResponse, DefaultError]]:
        return await _create_folders_async(
            client=self.client,
            body=body,
        )

    def create_shared_links(
        self,
        *,
        body: CreateSharedLinksRequest,
    ) -> Optional[Union[CreateSharedLinksResponse, DefaultError]]:
        return _create_shared_links(
            client=self.client,
            body=body,
        )

    async def create_shared_links_async(
        self,
        *,
        body: CreateSharedLinksRequest,
    ) -> Optional[Union[CreateSharedLinksResponse, DefaultError]]:
        return await _create_shared_links_async(
            client=self.client,
            body=body,
        )

    def delete_file(
        self,
        *,
        parent_rev: Optional[str] = None,
        file_path: str,
        file_path_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_file(
            client=self.client,
            parent_rev=parent_rev,
            file_path=file_path,
            file_path_lookup=file_path_lookup,
        )

    async def delete_file_async(
        self,
        *,
        parent_rev: Optional[str] = None,
        file_path: str,
        file_path_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_file_async(
            client=self.client,
            parent_rev=parent_rev,
            file_path=file_path,
            file_path_lookup=file_path_lookup,
        )

    def delete_folders(
        self,
        *,
        folder_path: str,
        folder_path_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return _delete_folders(
            client=self.client,
            folder_path=folder_path,
            folder_path_lookup=folder_path_lookup,
        )

    async def delete_folders_async(
        self,
        *,
        folder_path: str,
        folder_path_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _delete_folders_async(
            client=self.client,
            folder_path=folder_path,
            folder_path_lookup=folder_path_lookup,
        )

    def file_downloads(
        self,
        *,
        file_id_or_path: str,
        file_id_or_path_lookup: Any,
    ) -> Optional[Union[DefaultError, File]]:
        return _file_downloads(
            client=self.client,
            file_id_or_path=file_id_or_path,
            file_id_or_path_lookup=file_id_or_path_lookup,
        )

    async def file_downloads_async(
        self,
        *,
        file_id_or_path: str,
        file_id_or_path_lookup: Any,
    ) -> Optional[Union[DefaultError, File]]:
        return await _file_downloads_async(
            client=self.client,
            file_id_or_path=file_id_or_path,
            file_id_or_path_lookup=file_id_or_path_lookup,
        )

    def file_uploads(
        self,
        *,
        body: FileUploadsBody,
    ) -> Optional[Union[DefaultError, FileUploadsResponse]]:
        return _file_uploads(
            client=self.client,
            body=body,
        )

    async def file_uploads_async(
        self,
        *,
        body: FileUploadsBody,
    ) -> Optional[Union[DefaultError, FileUploadsResponse]]:
        return await _file_uploads_async(
            client=self.client,
            body=body,
        )

    def files_search(
        self,
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
        path_lookup: Any,
    ) -> Optional[Union[DefaultError, list["FilesSearch"]]]:
        return _files_search(
            client=self.client,
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

    async def files_search_async(
        self,
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
        path_lookup: Any,
    ) -> Optional[Union[DefaultError, list["FilesSearch"]]]:
        return await _files_search_async(
            client=self.client,
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

    def get_file_details(
        self,
        *,
        include_media_info: Optional[bool] = None,
        include_deleted: Optional[bool] = None,
        include_has_explicit_shared_members: Optional[bool] = None,
        file_path: str,
        file_path_lookup: Any,
    ) -> Optional[Union[DefaultError, GetFileDetailsResponse]]:
        return _get_file_details(
            client=self.client,
            include_media_info=include_media_info,
            include_deleted=include_deleted,
            include_has_explicit_shared_members=include_has_explicit_shared_members,
            file_path=file_path,
            file_path_lookup=file_path_lookup,
        )

    async def get_file_details_async(
        self,
        *,
        include_media_info: Optional[bool] = None,
        include_deleted: Optional[bool] = None,
        include_has_explicit_shared_members: Optional[bool] = None,
        file_path: str,
        file_path_lookup: Any,
    ) -> Optional[Union[DefaultError, GetFileDetailsResponse]]:
        return await _get_file_details_async(
            client=self.client,
            include_media_info=include_media_info,
            include_deleted=include_deleted,
            include_has_explicit_shared_members=include_has_explicit_shared_members,
            file_path=file_path,
            file_path_lookup=file_path_lookup,
        )

    def get_folder_content(
        self,
        *,
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
        return _get_folder_content(
            client=self.client,
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

    async def get_folder_content_async(
        self,
        *,
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
        return await _get_folder_content_async(
            client=self.client,
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

    def get_shared_link(
        self,
        *,
        path: str,
        path_lookup: Any,
    ) -> Optional[Union[DefaultError, GetSharedLinkResponse]]:
        return _get_shared_link(
            client=self.client,
            path=path,
            path_lookup=path_lookup,
        )

    async def get_shared_link_async(
        self,
        *,
        path: str,
        path_lookup: Any,
    ) -> Optional[Union[DefaultError, GetSharedLinkResponse]]:
        return await _get_shared_link_async(
            client=self.client,
            path=path,
            path_lookup=path_lookup,
        )

    def suspend_members(
        self,
        id_lookup: Any,
        id: str,
        *,
        wipe_data: Optional[bool] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return _suspend_members(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
            wipe_data=wipe_data,
        )

    async def suspend_members_async(
        self,
        id_lookup: Any,
        id: str,
        *,
        wipe_data: Optional[bool] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _suspend_members_async(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
            wipe_data=wipe_data,
        )

    def unsuspendmembers(
        self,
        id_lookup: Any,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _unsuspendmembers(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )

    async def unsuspendmembers_async(
        self,
        id_lookup: Any,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _unsuspendmembers_async(
            client=self.client,
            id=id,
            id_lookup=id_lookup,
        )
