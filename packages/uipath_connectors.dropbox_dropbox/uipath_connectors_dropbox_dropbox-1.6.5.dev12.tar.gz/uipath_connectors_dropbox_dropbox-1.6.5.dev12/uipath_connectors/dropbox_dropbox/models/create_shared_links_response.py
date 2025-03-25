from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_shared_links_response_content_owner_team_info import (
    CreateSharedLinksResponseContentOwnerTeamInfo,
)
from ..models.create_shared_links_response_link_permissions import (
    CreateSharedLinksResponseLinkPermissions,
)
from ..models.create_shared_links_response_team_member_info import (
    CreateSharedLinksResponseTeamMemberInfo,
)
import datetime


class CreateSharedLinksResponse(BaseModel):
    """
    Attributes:
        client_modified (Optional[datetime.datetime]):  Example: 2015-05-12T15:50:38Z.
        content_owner_team_info (Optional[CreateSharedLinksResponseContentOwnerTeamInfo]):
        expires (Optional[datetime.datetime]):  Example: 2021-07-12T15:50:38Z.
        id (Optional[str]):  Example: id:a4ayc_80_OEAAAAAAAAAXw.
        link_permissions (Optional[CreateSharedLinksResponseLinkPermissions]):
        name (Optional[str]):  Example: Math.
        path_lower (Optional[str]):  Example: /homework/math.
        rev (Optional[str]):  Example: a1c10ce0dd78.
        server_modified (Optional[datetime.datetime]):  Example: 2015-05-12T15:50:38Z.
        size (Optional[int]):  Example: 7212.0.
        tag (Optional[str]):  Example: folder.
        team_member_info (Optional[CreateSharedLinksResponseTeamMemberInfo]):
        url (Optional[str]): Shared link Example:
                https://www.dropbox.com/sh/s6fvw6ol7rmqo1x/AAAgWRSbjmYDvPpDB30Sykjfa?dl=0.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    client_modified: Optional[datetime.datetime] = Field(
        alias="client_modified", default=None
    )
    content_owner_team_info: Optional[
        "CreateSharedLinksResponseContentOwnerTeamInfo"
    ] = Field(alias="content_owner_team_info", default=None)
    expires: Optional[datetime.datetime] = Field(alias="expires", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    link_permissions: Optional["CreateSharedLinksResponseLinkPermissions"] = Field(
        alias="link_permissions", default=None
    )
    name: Optional[str] = Field(alias="name", default=None)
    path_lower: Optional[str] = Field(alias="path_lower", default=None)
    rev: Optional[str] = Field(alias="rev", default=None)
    server_modified: Optional[datetime.datetime] = Field(
        alias="server_modified", default=None
    )
    size: Optional[int] = Field(alias="size", default=None)
    tag: Optional[str] = Field(alias="tag", default=None)
    team_member_info: Optional["CreateSharedLinksResponseTeamMemberInfo"] = Field(
        alias="team_member_info", default=None
    )
    url: Optional[str] = Field(alias="url", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateSharedLinksResponse"], src_dict: Dict[str, Any]):
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
