from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_shared_link_response_link_permissions import (
    GetSharedLinkResponseLinkPermissions,
)
import datetime


class GetSharedLinkResponse(BaseModel):
    """
    Attributes:
        client_modified (Optional[datetime.datetime]):  Example: 2022-07-09T05:02:08Z.
        id (Optional[str]):  Example: id:PdvXlCWm-7wAAAAAAABKaw.
        link_permissions (Optional[GetSharedLinkResponseLinkPermissions]):
        name (Optional[str]):  Example: Dropbox.json.
        path_lower (Optional[str]):  Example: /uipath_purchase_orders/dropbox.json.
        preview_type (Optional[str]):  Example: text.
        rev (Optional[str]):  Example: 015e3e46820d8f6000000027593ca70.
        server_modified (Optional[datetime.datetime]):  Example: 2022-07-16T04:17:02Z.
        size (Optional[int]):  Example: 87150.0.
        tag (Optional[str]):  Example: file.
        url (Optional[str]):  Example: https://www.dropbox.com/s/wf0vth9eilqkwsf/Dropbox.json?dl=0.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    client_modified: Optional[datetime.datetime] = Field(
        alias="client_modified", default=None
    )
    id: Optional[str] = Field(alias="id", default=None)
    link_permissions: Optional["GetSharedLinkResponseLinkPermissions"] = Field(
        alias="link_permissions", default=None
    )
    name: Optional[str] = Field(alias="name", default=None)
    path_lower: Optional[str] = Field(alias="path_lower", default=None)
    preview_type: Optional[str] = Field(alias="preview_type", default=None)
    rev: Optional[str] = Field(alias="rev", default=None)
    server_modified: Optional[datetime.datetime] = Field(
        alias="server_modified", default=None
    )
    size: Optional[int] = Field(alias="size", default=None)
    tag: Optional[str] = Field(alias="tag", default=None)
    url: Optional[str] = Field(alias="url", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetSharedLinkResponse"], src_dict: Dict[str, Any]):
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
