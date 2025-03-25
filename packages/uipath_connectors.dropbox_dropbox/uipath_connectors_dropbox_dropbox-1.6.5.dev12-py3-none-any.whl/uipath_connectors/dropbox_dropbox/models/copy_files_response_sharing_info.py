from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class CopyFilesResponseSharingInfo(BaseModel):
    """
    Attributes:
        modified_by (Optional[str]):  Example: dbid:AAH4f99T0taONIb-OurWxbNQ6ywGRopQngc.
        parent_shared_folder_id (Optional[str]):  Example: 84528192421.
        read_only (Optional[bool]):  Example: True.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    modified_by: Optional[str] = Field(alias="modified_by", default=None)
    parent_shared_folder_id: Optional[str] = Field(
        alias="parent_shared_folder_id", default=None
    )
    read_only: Optional[bool] = Field(alias="read_only", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CopyFilesResponseSharingInfo"], src_dict: Dict[str, Any]):
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
