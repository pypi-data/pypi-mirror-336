from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_members_profile_membership_type import (
    ListMembersProfileMembershipType,
)
from ..models.list_members_profile_name import ListMembersProfileName
from ..models.list_members_profile_secondary_emails_array_item_ref import (
    ListMembersProfileSecondaryEmailsArrayItemRef,
)
from ..models.list_members_profile_status import ListMembersProfileStatus
import datetime


class ListMembersProfile(BaseModel):
    """
    Attributes:
        account_id (Optional[str]):  Example: dbid:AAH4f99T0taONIb-OurWxbNQ6ywGRopQngc.
        email (Optional[str]):  Example: tami@seagull.com.
        email_verified (Optional[bool]):
        external_id (Optional[str]):  Example: 244423.
        groups (Optional[list[str]]):
        joined_on (Optional[datetime.datetime]):  Example: 2015-05-12T15:50:38Z.
        member_folder_id (Optional[str]):  Example: 20.
        membership_type (Optional[ListMembersProfileMembershipType]):
        name (Optional[ListMembersProfileName]):
        profile_photo_url (Optional[str]):  Example: https://dl-
                web.dropbox.com/account_photo/get/dbaphid%3AAAHWGmIXV3sUuOmBfTz0wPsiqHUpBWvv3ZA?vers=1556069330102&size=128x128.
        secondary_emails (Optional[list['ListMembersProfileSecondaryEmailsArrayItemRef']]):
        status (Optional[ListMembersProfileStatus]):
        team_member_id (Optional[str]):  Example: dbmid:FDFSVF-DFSDF.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account_id: Optional[str] = Field(alias="account_id", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    email_verified: Optional[bool] = Field(alias="email_verified", default=None)
    external_id: Optional[str] = Field(alias="external_id", default=None)
    groups: Optional[list[str]] = Field(alias="groups", default=None)
    joined_on: Optional[datetime.datetime] = Field(alias="joined_on", default=None)
    member_folder_id: Optional[str] = Field(alias="member_folder_id", default=None)
    membership_type: Optional["ListMembersProfileMembershipType"] = Field(
        alias="membership_type", default=None
    )
    name: Optional["ListMembersProfileName"] = Field(alias="name", default=None)
    profile_photo_url: Optional[str] = Field(alias="profile_photo_url", default=None)
    secondary_emails: Optional[
        list["ListMembersProfileSecondaryEmailsArrayItemRef"]
    ] = Field(alias="secondary_emails", default=None)
    status: Optional["ListMembersProfileStatus"] = Field(alias="status", default=None)
    team_member_id: Optional[str] = Field(alias="team_member_id", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListMembersProfile"], src_dict: Dict[str, Any]):
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
