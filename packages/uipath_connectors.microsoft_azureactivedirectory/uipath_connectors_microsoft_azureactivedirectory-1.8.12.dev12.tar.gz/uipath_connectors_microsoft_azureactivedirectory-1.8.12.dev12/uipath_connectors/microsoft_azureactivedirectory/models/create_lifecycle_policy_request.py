from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_lifecycle_policy_request_managed_group_types import (
    CreateLifecyclePolicyRequestManagedGroupTypes,
)


class CreateLifecyclePolicyRequest(BaseModel):
    """
    Attributes:
        alternate_notification_email (str): An email address for sending notifications about the policy.
        group_lifetime_in_days (int): The number of days before a group expires and needs to be renewed.
        managed_group_types (Optional[CreateLifecyclePolicyRequestManagedGroupTypes]): The group type for which the
                expiration policy applies.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alternate_notification_email: str = Field(alias="alternateNotificationEmail")
    group_lifetime_in_days: int = Field(alias="groupLifetimeInDays")
    managed_group_types: Optional["CreateLifecyclePolicyRequestManagedGroupTypes"] = (
        Field(alias="managedGroupTypes", default=None)
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateLifecyclePolicyRequest"], src_dict: Dict[str, Any]):
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
