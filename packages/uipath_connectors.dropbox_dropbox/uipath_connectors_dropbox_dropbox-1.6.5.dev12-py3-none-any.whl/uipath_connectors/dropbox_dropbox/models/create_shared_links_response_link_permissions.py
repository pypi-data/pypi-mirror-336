from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_shared_links_response_link_permissions_audience_options_array_item_ref import (
    CreateSharedLinksResponseLinkPermissionsAudienceOptionsArrayItemRef,
)
from ..models.create_shared_links_response_link_permissions_resolved_visibility import (
    CreateSharedLinksResponseLinkPermissionsResolvedVisibility,
)
from ..models.create_shared_links_response_link_permissions_revoke_failure_reason import (
    CreateSharedLinksResponseLinkPermissionsRevokeFailureReason,
)
from ..models.create_shared_links_response_link_permissions_visibility_policies_array_item_ref import (
    CreateSharedLinksResponseLinkPermissionsVisibilityPoliciesArrayItemRef,
)


class CreateSharedLinksResponseLinkPermissions(BaseModel):
    """
    Attributes:
        allow_comments (Optional[bool]):  Example: True.
        allow_download (Optional[bool]):  Example: True.
        audience_options (Optional[list['CreateSharedLinksResponseLinkPermissionsAudienceOptionsArrayItemRef']]):
        can_allow_download (Optional[bool]):  Example: True.
        can_disallow_download (Optional[bool]):
        can_remove_expiry (Optional[bool]):
        can_remove_password (Optional[bool]):  Example: True.
        can_revoke (Optional[bool]):
        can_set_expiry (Optional[bool]):
        can_set_password (Optional[bool]):  Example: True.
        can_use_extended_sharing_controls (Optional[bool]):
        require_password (Optional[bool]):
        resolved_visibility (Optional[CreateSharedLinksResponseLinkPermissionsResolvedVisibility]):
        revoke_failure_reason (Optional[CreateSharedLinksResponseLinkPermissionsRevokeFailureReason]):
        team_restricts_comments (Optional[bool]):  Example: True.
        visibility_policies (Optional[list['CreateSharedLinksResponseLinkPermissionsVisibilityPoliciesArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    allow_comments: Optional[bool] = Field(alias="allow_comments", default=None)
    allow_download: Optional[bool] = Field(alias="allow_download", default=None)
    audience_options: Optional[
        list["CreateSharedLinksResponseLinkPermissionsAudienceOptionsArrayItemRef"]
    ] = Field(alias="audience_options", default=None)
    can_allow_download: Optional[bool] = Field(alias="can_allow_download", default=None)
    can_disallow_download: Optional[bool] = Field(
        alias="can_disallow_download", default=None
    )
    can_remove_expiry: Optional[bool] = Field(alias="can_remove_expiry", default=None)
    can_remove_password: Optional[bool] = Field(
        alias="can_remove_password", default=None
    )
    can_revoke: Optional[bool] = Field(alias="can_revoke", default=None)
    can_set_expiry: Optional[bool] = Field(alias="can_set_expiry", default=None)
    can_set_password: Optional[bool] = Field(alias="can_set_password", default=None)
    can_use_extended_sharing_controls: Optional[bool] = Field(
        alias="can_use_extended_sharing_controls", default=None
    )
    require_password: Optional[bool] = Field(alias="require_password", default=None)
    resolved_visibility: Optional[
        "CreateSharedLinksResponseLinkPermissionsResolvedVisibility"
    ] = Field(alias="resolved_visibility", default=None)
    revoke_failure_reason: Optional[
        "CreateSharedLinksResponseLinkPermissionsRevokeFailureReason"
    ] = Field(alias="revoke_failure_reason", default=None)
    team_restricts_comments: Optional[bool] = Field(
        alias="team_restricts_comments", default=None
    )
    visibility_policies: Optional[
        list["CreateSharedLinksResponseLinkPermissionsVisibilityPoliciesArrayItemRef"]
    ] = Field(alias="visibility_policies", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateSharedLinksResponseLinkPermissions"], src_dict: Dict[str, Any]
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
