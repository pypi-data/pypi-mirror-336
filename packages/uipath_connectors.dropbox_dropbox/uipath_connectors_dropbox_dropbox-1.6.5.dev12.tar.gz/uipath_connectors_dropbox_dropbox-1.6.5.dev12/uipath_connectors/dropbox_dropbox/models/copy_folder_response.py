from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.copy_folder_response_property_groups_array_item_ref import (
    CopyFolderResponsePropertyGroupsArrayItemRef,
)
from ..models.copy_folder_response_sharing_info import CopyFolderResponseSharingInfo


class CopyFolderResponse(BaseModel):
    """
    Attributes:
        name (str): Name of the file copy being created. If the parent folder is the same, this needs to be different
                than the original. Example: Prime_Numbers.txt.
        id (Optional[str]): File ID of the File copy Example: id:a4ayc_80_OEAAAAAAAAAXw.
        path_display (Optional[str]): Destination path Example: /Homework/math/Prime_Numbers.txt.
        path_lower (Optional[str]):  Example: /homework/math/prime_numbers.txt.
        property_groups (Optional[list['CopyFolderResponsePropertyGroupsArrayItemRef']]):
        sharing_info (Optional[CopyFolderResponseSharingInfo]):
        tag (Optional[str]):  Example: file.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str = Field(alias="name")
    id: Optional[str] = Field(alias="id", default=None)
    path_display: Optional[str] = Field(alias="path_display", default=None)
    path_lower: Optional[str] = Field(alias="path_lower", default=None)
    property_groups: Optional[list["CopyFolderResponsePropertyGroupsArrayItemRef"]] = (
        Field(alias="property_groups", default=None)
    )
    sharing_info: Optional["CopyFolderResponseSharingInfo"] = Field(
        alias="sharing_info", default=None
    )
    tag: Optional[str] = Field(alias="tag", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CopyFolderResponse"], src_dict: Dict[str, Any]):
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
