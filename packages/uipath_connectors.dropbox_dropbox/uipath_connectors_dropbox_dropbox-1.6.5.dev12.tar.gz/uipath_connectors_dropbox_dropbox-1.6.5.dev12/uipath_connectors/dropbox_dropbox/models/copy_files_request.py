from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class CopyFilesRequest(BaseModel):
    """
    Attributes:
        from_path (str): It is the path in the user's Dropbox that is the source. Pattern DirectPath | ns:.|id:. ,sample
                value :/Homework/algebra. Example: /Homework/math.
        to_path (str): It is the path in the user's Dropbox that is the destination. Pattern DirectPath | ns:.|id:.
                ,sample value :/Homework/algebra. Example: /Homework/algebra.
        allow_ownership_transfer (Optional[bool]): If set to True, the ownership of the file can be changed. If False,
                ownership will be limited to user executing the copy
        autorename (Optional[bool]): Auto-renames the file if there is a conflict Default: False.
        name (Optional[str]):  Example: Prime_Numbers.txt.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    from_path: str = Field(alias="from_path")
    to_path: str = Field(alias="to_path")
    allow_ownership_transfer: Optional[bool] = Field(
        alias="allow_ownership_transfer", default=None
    )
    autorename: Optional[bool] = Field(alias="autorename", default=False)
    name: Optional[str] = Field(alias="name", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CopyFilesRequest"], src_dict: Dict[str, Any]):
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
