from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class GetGroupByNameResponse(BaseModel):
    """
    Attributes:
        classification (Optional[str]): Indicates the classification level of the group. Example: General.
        created_date_time (Optional[datetime.datetime]): The date and time when the group was created. Example:
                2024-10-03T18:08:40Z.
        deleted_date_time (Optional[datetime.datetime]): The date and time when the group was deleted. Example:
                1970-01-01T00:00:00Z.
        description (Optional[str]): A brief description of the group. Example: 2Self help community for library.
        display_name (Optional[str]): The name displayed for the group in Azure AD. Example: Library Assist4.
        expiration_date_time (Optional[datetime.datetime]): The date and time when the group will expire. Example:
                1970-01-01T00:00:00Z.
        group_types (Optional[list[str]]):
        id (Optional[str]): A unique identifier for the group. Example: c6772abb-f2fb-40aa-a724-6504f5ff27db.
        is_assignable_to_role (Optional[bool]): Specifies if the group can be assigned to a role.
        mail (Optional[str]): The email address associated with the group.
        mail_enabled (Optional[bool]): Indicates if the group is mail-enabled.
        mail_nickname (Optional[str]): The email alias or nickname for the group. Example: library4.
        membership_rule (Optional[str]): The rule that defines the group's membership criteria.
        membership_rule_processing_state (Optional[str]): The current state of the membership rule processing. Example:
                NotProcessing.
        on_premises_domain_name (Optional[str]): The domain name of the group in on-premises systems.
        on_premises_last_sync_date_time (Optional[datetime.datetime]): The date and time when the last sync with on-
                premises occurred. Example: 1970-01-01T00:00:00Z.
        on_premises_net_bios_name (Optional[str]): The NetBIOS name of the group in on-premises systems.
        on_premises_sam_account_name (Optional[str]): The SAM account name for the group in on-premises directory.
        on_premises_security_identifier (Optional[str]): The security identifier for the group in on-premises systems.
        on_premises_sync_enabled (Optional[bool]): Indicates if the group is synced with on-premises directory.
        preferred_data_location (Optional[str]): The preferred location for storing the group's data. Example: global.
        preferred_language (Optional[str]): The language preference for the group. Example: en-US.
        proxy_addresses (Optional[list[str]]):
        renewed_date_time (Optional[datetime.datetime]): The date and time when the group was last renewed. Example:
                2024-10-03T18:08:40Z.
        security_enabled (Optional[bool]): Indicates if the group has security features enabled. Example: True.
        security_identifier (Optional[str]): A unique identifier for the security object. Example:
                S-1-12-1-3329698491-1084945147-73737383-3676831733.
        theme (Optional[str]): The visual theme or style associated with the group. Example: default.
        unique_name (Optional[str]): A unique name assigned to the group for identification.
        visibility (Optional[str]): Indicates whether the group is public or private. Example: Public.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    classification: Optional[str] = Field(alias="classification", default=None)
    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    deleted_date_time: Optional[datetime.datetime] = Field(
        alias="deletedDateTime", default=None
    )
    description: Optional[str] = Field(alias="description", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    expiration_date_time: Optional[datetime.datetime] = Field(
        alias="expirationDateTime", default=None
    )
    group_types: Optional[list[str]] = Field(alias="groupTypes", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    is_assignable_to_role: Optional[bool] = Field(
        alias="isAssignableToRole", default=None
    )
    mail: Optional[str] = Field(alias="mail", default=None)
    mail_enabled: Optional[bool] = Field(alias="mailEnabled", default=None)
    mail_nickname: Optional[str] = Field(alias="mailNickname", default=None)
    membership_rule: Optional[str] = Field(alias="membershipRule", default=None)
    membership_rule_processing_state: Optional[str] = Field(
        alias="membershipRuleProcessingState", default=None
    )
    on_premises_domain_name: Optional[str] = Field(
        alias="onPremisesDomainName", default=None
    )
    on_premises_last_sync_date_time: Optional[datetime.datetime] = Field(
        alias="onPremisesLastSyncDateTime", default=None
    )
    on_premises_net_bios_name: Optional[str] = Field(
        alias="onPremisesNetBiosName", default=None
    )
    on_premises_sam_account_name: Optional[str] = Field(
        alias="onPremisesSamAccountName", default=None
    )
    on_premises_security_identifier: Optional[str] = Field(
        alias="onPremisesSecurityIdentifier", default=None
    )
    on_premises_sync_enabled: Optional[bool] = Field(
        alias="onPremisesSyncEnabled", default=None
    )
    preferred_data_location: Optional[str] = Field(
        alias="preferredDataLocation", default=None
    )
    preferred_language: Optional[str] = Field(alias="preferredLanguage", default=None)
    proxy_addresses: Optional[list[str]] = Field(alias="proxyAddresses", default=None)
    renewed_date_time: Optional[datetime.datetime] = Field(
        alias="renewedDateTime", default=None
    )
    security_enabled: Optional[bool] = Field(alias="securityEnabled", default=None)
    security_identifier: Optional[str] = Field(alias="securityIdentifier", default=None)
    theme: Optional[str] = Field(alias="theme", default=None)
    unique_name: Optional[str] = Field(alias="uniqueName", default=None)
    visibility: Optional[str] = Field(alias="visibility", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetGroupByNameResponse"], src_dict: Dict[str, Any]):
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
