from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.add_members_response_complete_profile_membership_type import (
    AddMembersResponseCompleteProfileMembershipType,
)
from ..models.add_members_response_complete_profile_name import (
    AddMembersResponseCompleteProfileName,
)
from ..models.add_members_response_complete_profile_status import (
    AddMembersResponseCompleteProfileStatus,
)
import datetime


class AddMembersResponseCompleteProfile(BaseModel):
    """
    Attributes:
        account_id (Optional[str]):  Example: dbid:AACsJ5VLR0BoLyTV6YAnpTqmTzs_szmh-EQ.
        email (Optional[str]):  Example: lavish.yadav@uipath.com.
        email_verified (Optional[bool]):
        groups (Optional[list[str]]):
        invited_on (Optional[datetime.datetime]):  Example: 2022-11-09T07:18:55Z.
        member_folder_id (Optional[str]):  Example: 10780180448.
        membership_type (Optional[AddMembersResponseCompleteProfileMembershipType]):
        name (Optional[AddMembersResponseCompleteProfileName]):
        status (Optional[AddMembersResponseCompleteProfileStatus]):
        team_member_id (Optional[str]):  Example: dbmid:AABHqKe00JosNdCcKlFbErpJO7ciZkrot4Y.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account_id: Optional[str] = Field(alias="account_id", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    email_verified: Optional[bool] = Field(alias="email_verified", default=None)
    groups: Optional[list[str]] = Field(alias="groups", default=None)
    invited_on: Optional[datetime.datetime] = Field(alias="invited_on", default=None)
    member_folder_id: Optional[str] = Field(alias="member_folder_id", default=None)
    membership_type: Optional["AddMembersResponseCompleteProfileMembershipType"] = (
        Field(alias="membership_type", default=None)
    )
    name: Optional["AddMembersResponseCompleteProfileName"] = Field(
        alias="name", default=None
    )
    status: Optional["AddMembersResponseCompleteProfileStatus"] = Field(
        alias="status", default=None
    )
    team_member_id: Optional[str] = Field(alias="team_member_id", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AddMembersResponseCompleteProfile"], src_dict: Dict[str, Any]
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
