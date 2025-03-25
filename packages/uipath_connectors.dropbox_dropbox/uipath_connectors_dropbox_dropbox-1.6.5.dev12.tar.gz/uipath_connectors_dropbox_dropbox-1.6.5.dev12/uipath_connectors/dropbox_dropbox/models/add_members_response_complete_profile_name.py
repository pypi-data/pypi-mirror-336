from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class AddMembersResponseCompleteProfileName(BaseModel):
    """
    Attributes:
        abbreviated_name (Optional[str]):
        display_name (Optional[str]):
        familiar_name (Optional[str]):
        given_name (Optional[str]):
        surname (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    abbreviated_name: Optional[str] = Field(alias="abbreviated_name", default=None)
    display_name: Optional[str] = Field(alias="display_name", default=None)
    familiar_name: Optional[str] = Field(alias="familiar_name", default=None)
    given_name: Optional[str] = Field(alias="given_name", default=None)
    surname: Optional[str] = Field(alias="surname", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AddMembersResponseCompleteProfileName"], src_dict: Dict[str, Any]
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
