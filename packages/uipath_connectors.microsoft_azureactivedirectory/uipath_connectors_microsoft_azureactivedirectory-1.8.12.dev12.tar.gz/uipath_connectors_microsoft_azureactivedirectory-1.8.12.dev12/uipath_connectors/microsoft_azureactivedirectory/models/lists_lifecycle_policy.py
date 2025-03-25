from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.lists_lifecycle_policy_managed_group_types import (
    ListsLifecyclePolicyManagedGroupTypes,
)


class ListsLifecyclePolicy(BaseModel):
    """
    Attributes:
        alternate_notification_emails (Optional[str]): A list of email addresses for policy notifications. Example:
                EthylBlackledge@HiltonMonda.com.
        group_lifetime_in_days (Optional[int]): The number of days before a group expires and needs to be renewed.
        id (Optional[str]): A unique identifier for the group lifecycle policy. Example:
                1499d5de-f453-461b-8499-2498bc2b2b0e.
        managed_group_types (Optional[ListsLifecyclePolicyManagedGroupTypes]): The group type for which the expiration
                policy applies.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    alternate_notification_emails: Optional[str] = Field(
        alias="alternateNotificationEmails", default=None
    )
    group_lifetime_in_days: Optional[int] = Field(
        alias="groupLifetimeInDays", default=None
    )
    id: Optional[str] = Field(alias="id", default=None)
    managed_group_types: Optional["ListsLifecyclePolicyManagedGroupTypes"] = Field(
        alias="managedGroupTypes", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListsLifecyclePolicy"], src_dict: Dict[str, Any]):
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
