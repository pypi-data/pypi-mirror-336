from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_shared_link_response_link_permissions_visibility_policies_disallowed_reason import (
    GetSharedLinkResponseLinkPermissionsVisibilityPoliciesDisallowedReason,
)
from ..models.get_shared_link_response_link_permissions_visibility_policies_policy import (
    GetSharedLinkResponseLinkPermissionsVisibilityPoliciesPolicy,
)
from ..models.get_shared_link_response_link_permissions_visibility_policies_resolved_policy import (
    GetSharedLinkResponseLinkPermissionsVisibilityPoliciesResolvedPolicy,
)


class GetSharedLinkResponseLinkPermissionsVisibilityPoliciesArrayItemRef(BaseModel):
    """
    Attributes:
        allowed (Optional[bool]):  Example: True.
        disallowed_reason (Optional[GetSharedLinkResponseLinkPermissionsVisibilityPoliciesDisallowedReason]):
        policy (Optional[GetSharedLinkResponseLinkPermissionsVisibilityPoliciesPolicy]):
        resolved_policy (Optional[GetSharedLinkResponseLinkPermissionsVisibilityPoliciesResolvedPolicy]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    allowed: Optional[bool] = Field(alias="allowed", default=None)
    disallowed_reason: Optional[
        "GetSharedLinkResponseLinkPermissionsVisibilityPoliciesDisallowedReason"
    ] = Field(alias="disallowed_reason", default=None)
    policy: Optional["GetSharedLinkResponseLinkPermissionsVisibilityPoliciesPolicy"] = (
        Field(alias="policy", default=None)
    )
    resolved_policy: Optional[
        "GetSharedLinkResponseLinkPermissionsVisibilityPoliciesResolvedPolicy"
    ] = Field(alias="resolved_policy", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetSharedLinkResponseLinkPermissionsVisibilityPoliciesArrayItemRef"],
        src_dict: Dict[str, Any],
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
