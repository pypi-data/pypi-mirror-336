from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.file_uploads_request_property_groups_array_item_ref import (
    FileUploadsRequestPropertyGroupsArrayItemRef,
)


class FileUploadsRequest(BaseModel):
    """
    Attributes:
        path (str):  Example: /Homework/math/Matrices.txt.
        autorename (Optional[bool]): Auto-renames the file if there is a conflict
        content_hash (Optional[str]):  Example: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
        mode (Optional[str]):
        mute (Optional[bool]): Users are made aware of any file modifications in their Dropbox account via notifications
                in the client software
        name (Optional[str]):  Example: Prime_Numbers.txt.
        property_groups (Optional[list['FileUploadsRequestPropertyGroupsArrayItemRef']]):
        strict_conflict (Optional[bool]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    path: str = Field(alias="path")
    autorename: Optional[bool] = Field(alias="autorename", default=None)
    content_hash: Optional[str] = Field(alias="content_hash", default=None)
    mode: Optional[str] = Field(alias="mode", default=None)
    mute: Optional[bool] = Field(alias="mute", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    property_groups: Optional[list["FileUploadsRequestPropertyGroupsArrayItemRef"]] = (
        Field(alias="property_groups", default=None)
    )
    strict_conflict: Optional[bool] = Field(alias="strict_conflict", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["FileUploadsRequest"], src_dict: Dict[str, Any]):
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
