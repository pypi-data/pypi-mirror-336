from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListMembersRolesArrayItemRef(BaseModel):
    """
    Attributes:
        description (Optional[str]):  Example: Add, remove, and manage member accounts..
        name (Optional[str]):  Example: User management admin.
        role_id (Optional[str]):  Example: pid_dbtmr:3456.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: Optional[str] = Field(alias="description", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    role_id: Optional[str] = Field(alias="role_id", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListMembersRolesArrayItemRef"], src_dict: Dict[str, Any]):
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
