from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_folders_response_property_groups_fields_array_item_ref import (
    CreateFoldersResponsePropertyGroupsFieldsArrayItemRef,
)


class CreateFoldersResponsePropertyGroupsArrayItemRef(BaseModel):
    """
    Attributes:
        fields (Optional[list['CreateFoldersResponsePropertyGroupsFieldsArrayItemRef']]):
        template_id (Optional[str]):  Example: ptid:1a5n2i6d3OYEAAAAAAAAAYa.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    fields: Optional[list["CreateFoldersResponsePropertyGroupsFieldsArrayItemRef"]] = (
        Field(alias="fields", default=None)
    )
    template_id: Optional[str] = Field(alias="template_id", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateFoldersResponsePropertyGroupsArrayItemRef"],
        src_dict: Dict[str, Any],
    ):
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
