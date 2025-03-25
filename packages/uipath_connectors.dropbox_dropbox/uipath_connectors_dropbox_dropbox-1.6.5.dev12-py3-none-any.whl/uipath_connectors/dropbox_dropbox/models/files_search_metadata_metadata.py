from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class FilesSearchMetadataMetadata(BaseModel):
    """
    Attributes:
        client_modified (Optional[datetime.datetime]): The date and time the file was last modified by the client.
                Example: 2022-04-22T03:50:22Z.
        content_hash (Optional[str]): A hash of the file content, used to verify file integrity. Example:
                e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
        id (Optional[str]): A unique identifier for the file within Dropbox. Example: id:PdvXlCWm-7wAAAAAAABKbA.
        is_downloadable (Optional[bool]): Indicates if the file can be downloaded. Example: True.
        name (Optional[str]): The name of the file or folder without its path. Example: UiPath Connectors.
        path_display (Optional[str]): The complete path where the file or folder is located. Example: /UiPath
                Connectors.
        path_lower (Optional[str]): The full path to the file or folder, displayed in lowercase. Example: /uipath
                connectors.
        rev (Optional[str]): Unique identifier for the current revision of the file. Example:
                015dd36203d7ae300000002506a6280.
        server_modified (Optional[datetime.datetime]): The timestamp when the file was last modified on the server.
                Example: 2022-04-22T03:50:22Z.
        size (Optional[int]): The size of the file measured in bytes. Example: 3979.0.
        tag (Optional[str]): Indicates the type or category of the file. Example: folder.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    client_modified: Optional[datetime.datetime] = Field(
        alias="client_modified", default=None
    )
    content_hash: Optional[str] = Field(alias="content_hash", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    is_downloadable: Optional[bool] = Field(alias="is_downloadable", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    path_display: Optional[str] = Field(alias="path_display", default=None)
    path_lower: Optional[str] = Field(alias="path_lower", default=None)
    rev: Optional[str] = Field(alias="rev", default=None)
    server_modified: Optional[datetime.datetime] = Field(
        alias="server_modified", default=None
    )
    size: Optional[int] = Field(alias="size", default=None)
    tag: Optional[str] = Field(alias="tag", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["FilesSearchMetadataMetadata"], src_dict: Dict[str, Any]):
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
