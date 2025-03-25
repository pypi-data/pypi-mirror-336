from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class ListAllGroupsInGroup(BaseModel):
    """
    Attributes:
        created_date_time (Optional[datetime.datetime]): The date and time when the group was created. Example:
                2021-11-24T13:56:59Z.
        display_name (Optional[str]): The name displayed for the group. Example: #test_ad_group.
        id (Optional[str]): Unique identifier for the group. Example: 634853c0-4498-4e23-8650-6deb65867957.
        mail_enabled (Optional[bool]): Indicates if the group is mail-enabled.
        mail_nickname (Optional[str]): The mail alias for the group. Example: _test_ad_group.
        odata_type (Optional[str]): The Odata type Example: #microsoft.graph.group.
        on_premises_domain_name (Optional[str]): The domain name of the group in on-premises systems. Example: test.rpa.
        on_premises_last_sync_date_time (Optional[datetime.datetime]): The last date and time the group was synced on-
                premises. Example: 2024-02-28T05:04:17Z.
        on_premises_net_bios_name (Optional[str]): The NetBIOS name for on-premises integration. Example: TEST.
        on_premises_sam_account_name (Optional[str]): The SAM account name of the group in on-premises systems. Example:
                #test_ad_group.
        on_premises_security_identifier (Optional[str]): Unique identifier for the group in on-premises systems.
                Example: S-1-5-21-2332796148-3810505397-805562664-1254.
        on_premises_sync_enabled (Optional[bool]): Indicates if the group is synchronized with on-premises directory.
                Example: True.
        renewed_date_time (Optional[datetime.datetime]): The date and time when the group was last renewed. Example:
                2021-11-24T13:56:59Z.
        security_enabled (Optional[bool]): Indicates if the group is security-enabled. Example: True.
        security_identifier (Optional[str]): Unique identifier for security purposes. Example:
                S-1-12-1-1665684416-1310934168-3949809798-1467582053.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    display_name: Optional[str] = Field(alias="displayName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    mail_enabled: Optional[bool] = Field(alias="mailEnabled", default=None)
    mail_nickname: Optional[str] = Field(alias="mailNickname", default=None)
    odata_type: Optional[str] = Field(alias="odata_type", default=None)
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
    renewed_date_time: Optional[datetime.datetime] = Field(
        alias="renewedDateTime", default=None
    )
    security_enabled: Optional[bool] = Field(alias="securityEnabled", default=None)
    security_identifier: Optional[str] = Field(alias="securityIdentifier", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListAllGroupsInGroup"], src_dict: Dict[str, Any]):
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
