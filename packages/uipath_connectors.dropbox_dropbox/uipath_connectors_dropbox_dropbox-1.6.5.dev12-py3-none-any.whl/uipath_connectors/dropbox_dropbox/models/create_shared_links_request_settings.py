from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_shared_links_request_settings_access import (
    CreateSharedLinksRequestSettingsAccess,
)
from ..models.create_shared_links_request_settings_audience import (
    CreateSharedLinksRequestSettingsAudience,
)


class CreateSharedLinksRequestSettings(BaseModel):
    """
    Attributes:
        access (Optional[CreateSharedLinksRequestSettingsAccess]): Level of access associated to the shared link
                Example: viewer.
        allow_download (Optional[bool]): Allow download Example: True.
        audience (Optional[CreateSharedLinksRequestSettingsAudience]): Audience for the shared link content Example:
                public.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Optional["CreateSharedLinksRequestSettingsAccess"] = Field(
        alias="access", default=None
    )
    allow_download: Optional[bool] = Field(alias="allow_download", default=None)
    audience: Optional["CreateSharedLinksRequestSettingsAudience"] = Field(
        alias="audience", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateSharedLinksRequestSettings"], src_dict: Dict[str, Any]
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
