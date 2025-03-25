from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class ListGroups(BaseModel):
    """
    Attributes:
        created_date_time (Optional[datetime.datetime]): The date and time when the group was created. Example:
                2023-10-02T06:15:32Z.
        description (Optional[str]): The description of the group. Example: o365_test_group_temp desc.
        display_name (Optional[str]): The display name of the group. Example:
                apitest2e83bfb3-7391-4b20-a125-a84ba7a718a4.
        group_types (Optional[list[str]]):
        id (Optional[str]): A unique identifier for the group. Example: 000f1dde-b510-4a50-801e-07d77e06f535.
        mail (Optional[str]): The email address associated with the group. Example:
                o365_test_group_temp_YAID5@uipathstaging.onmicrosoft.com.
        mail_enabled (Optional[bool]): Specifies whether the group is mail-enabled.
        mail_nickname (Optional[str]): The mail alias for the group. Example: ahwexusaiwarxk.
        on_premises_domain_name (Optional[str]): The domain name of the group in the on-premises directory. Example:
                test.rpa.
        on_premises_last_sync_date_time (Optional[datetime.datetime]): The date and time when the group was last synced
                with on-premises. Example: 2020-08-02T09:11:50Z.
        on_premises_net_bios_name (Optional[str]): The NetBIOS name of the group in the on-premises directory. Example:
                TEST.
        on_premises_sam_account_name (Optional[str]): The SAM account name used in on-premises environments. Example:
                $F31000-RG52PIKBHDF3.
        on_premises_security_identifier (Optional[str]): A unique ID used to identify the group in on-premises systems.
                Example: S-1-5-21-2332796148-3810505397-805562664-1126.
        on_premises_sync_enabled (Optional[bool]): Indicates if the group is synchronized with on-premises directory.
                Example: True.
        proxy_addresses (Optional[list[str]]):
        renewed_date_time (Optional[datetime.datetime]): The date and time when the group was last renewed. Example:
                2023-10-02T06:15:32Z.
        security_enabled (Optional[bool]): Specifies whether the group is a security group. Example: True.
        security_identifier (Optional[str]): A unique identifier for the group used for security purposes. Example:
                S-1-12-1-990686-1246803216-3607568000-905250430.
        visibility (Optional[str]): The visibility of the group. Example: Public.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    description: Optional[str] = Field(alias="description", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    group_types: Optional[list[str]] = Field(alias="groupTypes", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    mail: Optional[str] = Field(alias="mail", default=None)
    mail_enabled: Optional[bool] = Field(alias="mailEnabled", default=None)
    mail_nickname: Optional[str] = Field(alias="mailNickname", default=None)
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
    proxy_addresses: Optional[list[str]] = Field(alias="proxyAddresses", default=None)
    renewed_date_time: Optional[datetime.datetime] = Field(
        alias="renewedDateTime", default=None
    )
    security_enabled: Optional[bool] = Field(alias="securityEnabled", default=None)
    security_identifier: Optional[str] = Field(alias="securityIdentifier", default=None)
    visibility: Optional[str] = Field(alias="visibility", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListGroups"], src_dict: Dict[str, Any]):
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
