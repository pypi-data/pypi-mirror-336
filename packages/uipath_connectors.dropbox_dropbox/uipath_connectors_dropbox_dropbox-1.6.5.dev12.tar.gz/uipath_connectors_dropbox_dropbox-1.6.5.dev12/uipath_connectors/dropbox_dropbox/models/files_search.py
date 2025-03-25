from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.files_search_match_type import FilesSearchMatchType
from ..models.files_search_metadata import FilesSearchMetadata
import datetime


class FilesSearch(BaseModel):
    """
    Attributes:
        match_type (Optional[FilesSearchMatchType]):
        match_type_tag (Optional[str]): Indicates how the file matched the search query. Example: filename.
        metadata (Optional[FilesSearchMetadata]):
        metadata_metadata_client_modified (Optional[datetime.datetime]): The timestamp when the file was last modified
                by the client. Example: 2023-12-19T11:51:14Z.
        metadata_metadata_content_hash (Optional[str]): A unique hash representing the file's content for comparison
                purposes. Example: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
        metadata_metadata_file_owner_team_encrypted_id (Optional[str]): Encrypted identifier for the team that owns the
                file. Example: dbtid:AACTXQ5GJ7RKGE8LuYfXTqseLqXRSMszmK4.
        metadata_metadata_id (Optional[str]): The unique identifier for the file or folder's metadata. Example:
                id:0yHse95wzE4AAAAAAAABTg.
        metadata_metadata_is_downloadable (Optional[bool]): Shows whether the file is available for download. Example:
                True.
        metadata_metadata_name (Optional[str]): The name of the file or folder without its path. Example: test2.png.
        metadata_metadata_path_display (Optional[str]): The complete path where the file or folder is located. Example:
                /Vali/hdjshd/test2.png.
        metadata_metadata_path_lower (Optional[str]): The full path to the file in lowercase. Example:
                /vali/hdjshd/test2.png.
        metadata_metadata_rev (Optional[str]): The revision number of the file, indicating changes. Example:
                0160e0951c77e0d0000000103607a81.
        metadata_metadata_server_modified (Optional[datetime.datetime]): The exact time when the file was modified on
                the server. Example: 2024-01-03T11:57:29Z.
        metadata_metadata_size (Optional[int]): The total size of the file in bytes. Example: 338231.0.
        metadata_metadata_tag (Optional[str]): Contains specific tag information related to the file's metadata.
                Example: file.
        metadata_tag (Optional[str]): A tag representing the type of metadata. Example: metadata.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    match_type: Optional["FilesSearchMatchType"] = Field(
        alias="match_type", default=None
    )
    match_type_tag: Optional[str] = Field(alias="match_type_tag", default=None)
    metadata: Optional["FilesSearchMetadata"] = Field(alias="metadata", default=None)
    metadata_metadata_client_modified: Optional[datetime.datetime] = Field(
        alias="metadata_metadata_client_modified", default=None
    )
    metadata_metadata_content_hash: Optional[str] = Field(
        alias="metadata_metadata_content_hash", default=None
    )
    metadata_metadata_file_owner_team_encrypted_id: Optional[str] = Field(
        alias="metadata_metadata_file_owner_team_encrypted_id", default=None
    )
    metadata_metadata_id: Optional[str] = Field(
        alias="metadata_metadata_id", default=None
    )
    metadata_metadata_is_downloadable: Optional[bool] = Field(
        alias="metadata_metadata_is_downloadable", default=None
    )
    metadata_metadata_name: Optional[str] = Field(
        alias="metadata_metadata_name", default=None
    )
    metadata_metadata_path_display: Optional[str] = Field(
        alias="metadata_metadata_path_display", default=None
    )
    metadata_metadata_path_lower: Optional[str] = Field(
        alias="metadata_metadata_path_lower", default=None
    )
    metadata_metadata_rev: Optional[str] = Field(
        alias="metadata_metadata_rev", default=None
    )
    metadata_metadata_server_modified: Optional[datetime.datetime] = Field(
        alias="metadata_metadata_server_modified", default=None
    )
    metadata_metadata_size: Optional[int] = Field(
        alias="metadata_metadata_size", default=None
    )
    metadata_metadata_tag: Optional[str] = Field(
        alias="metadata_metadata_tag", default=None
    )
    metadata_tag: Optional[str] = Field(alias="metadata_tag", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["FilesSearch"], src_dict: Dict[str, Any]):
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
