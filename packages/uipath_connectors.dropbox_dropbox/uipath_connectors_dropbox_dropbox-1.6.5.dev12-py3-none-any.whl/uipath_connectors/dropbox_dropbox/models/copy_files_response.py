from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.copy_files_response_file_lock_info import CopyFilesResponseFileLockInfo
from ..models.copy_files_response_property_groups_array_item_ref import (
    CopyFilesResponsePropertyGroupsArrayItemRef,
)
from ..models.copy_files_response_sharing_info import CopyFilesResponseSharingInfo
import datetime


class CopyFilesResponse(BaseModel):
    """
    Attributes:
        client_modified (Optional[datetime.datetime]):  Example: 2015-05-12T15:50:38Z.
        content_hash (Optional[str]):  Example: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
        file_lock_info (Optional[CopyFilesResponseFileLockInfo]):
        has_explicit_shared_members (Optional[bool]):
        id (Optional[str]): File ID of the File copy Example: id:a4ayc_80_OEAAAAAAAAAXw.
        is_downloadable (Optional[bool]):  Example: True.
        name (Optional[str]):  Example: Prime_Numbers.txt.
        path_display (Optional[str]): Destination path Example: /Homework/math/Prime_Numbers.txt.
        path_lower (Optional[str]):  Example: /homework/math/prime_numbers.txt.
        property_groups (Optional[list['CopyFilesResponsePropertyGroupsArrayItemRef']]):
        rev (Optional[str]):  Example: a1c10ce0dd78.
        server_modified (Optional[datetime.datetime]):  Example: 2015-05-12T15:50:38Z.
        sharing_info (Optional[CopyFilesResponseSharingInfo]):
        size (Optional[int]):  Example: 7212.0.
        tag (Optional[str]):  Example: file.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    client_modified: Optional[datetime.datetime] = Field(
        alias="client_modified", default=None
    )
    content_hash: Optional[str] = Field(alias="content_hash", default=None)
    file_lock_info: Optional["CopyFilesResponseFileLockInfo"] = Field(
        alias="file_lock_info", default=None
    )
    has_explicit_shared_members: Optional[bool] = Field(
        alias="has_explicit_shared_members", default=None
    )
    id: Optional[str] = Field(alias="id", default=None)
    is_downloadable: Optional[bool] = Field(alias="is_downloadable", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    path_display: Optional[str] = Field(alias="path_display", default=None)
    path_lower: Optional[str] = Field(alias="path_lower", default=None)
    property_groups: Optional[list["CopyFilesResponsePropertyGroupsArrayItemRef"]] = (
        Field(alias="property_groups", default=None)
    )
    rev: Optional[str] = Field(alias="rev", default=None)
    server_modified: Optional[datetime.datetime] = Field(
        alias="server_modified", default=None
    )
    sharing_info: Optional["CopyFilesResponseSharingInfo"] = Field(
        alias="sharing_info", default=None
    )
    size: Optional[int] = Field(alias="size", default=None)
    tag: Optional[str] = Field(alias="tag", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CopyFilesResponse"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
