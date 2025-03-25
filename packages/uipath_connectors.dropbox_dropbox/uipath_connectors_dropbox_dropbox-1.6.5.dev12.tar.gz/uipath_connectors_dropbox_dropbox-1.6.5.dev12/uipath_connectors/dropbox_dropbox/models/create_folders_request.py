from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class CreateFoldersRequest(BaseModel):
    """
    Attributes:
        name (str): Name of the folder being created  Example: math.
        path (str): Select the location where the folder is to be created  Example: /Homework/math.
        autorename (Optional[bool]): Auto-renames the folder if there is a conflict
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str = Field(alias="name")
    path: str = Field(alias="path")
    autorename: Optional[bool] = Field(alias="autorename", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateFoldersRequest"], src_dict: Dict[str, Any]):
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
