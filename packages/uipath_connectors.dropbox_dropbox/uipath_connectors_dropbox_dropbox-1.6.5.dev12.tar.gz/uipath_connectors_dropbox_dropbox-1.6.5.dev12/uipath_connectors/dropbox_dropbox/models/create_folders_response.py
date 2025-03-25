from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_folders_response_property_groups_array_item_ref import (
    CreateFoldersResponsePropertyGroupsArrayItemRef,
)
from ..models.create_folders_response_sharing_info import (
    CreateFoldersResponseSharingInfo,
)


class CreateFoldersResponse(BaseModel):
    """
    Attributes:
        name (str): Name of the folder being created  Example: math.
        id (Optional[str]):  Example: id:a4ayc_80_OEAAAAAAAAAXz.
        path_display (Optional[str]): Created Folder path Example: /Homework/math.
        path_lower (Optional[str]):  Example: /homework/math.
        property_groups (Optional[list['CreateFoldersResponsePropertyGroupsArrayItemRef']]):
        sharing_info (Optional[CreateFoldersResponseSharingInfo]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str = Field(alias="name")
    id: Optional[str] = Field(alias="id", default=None)
    path_display: Optional[str] = Field(alias="path_display", default=None)
    path_lower: Optional[str] = Field(alias="path_lower", default=None)
    property_groups: Optional[
        list["CreateFoldersResponsePropertyGroupsArrayItemRef"]
    ] = Field(alias="property_groups", default=None)
    sharing_info: Optional["CreateFoldersResponseSharingInfo"] = Field(
        alias="sharing_info", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateFoldersResponse"], src_dict: Dict[str, Any]):
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
