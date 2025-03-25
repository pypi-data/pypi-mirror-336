from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class ListAllGroupsOfAUser(BaseModel):
    """
    Attributes:
        created_date_time (Optional[datetime.datetime]): The Created date time Example: 2019-10-11T11:22:00Z.
        creation_options (Optional[list[str]]):
        description (Optional[str]): A brief description of the user or group. Example: Can manage all aspects of the
                Power BI product..
        display_name (Optional[str]): The name displayed for the user or group. Example: Power BI Administrator.
        expiration_date_time (Optional[datetime.datetime]): The Expiration date time Example: 2019-12-09T00:00:00Z.
        group_types (Optional[list[str]]):
        id (Optional[str]): Unique identifier for the user or group. Example: 02c55166-f658-4a24-b222-b3080ee6b7ae.
        mail (Optional[str]): The Mail Example: TST1827@uipathstaging.onmicrosoft.com.
        mail_enabled (Optional[bool]): The Mail enabled
        mail_nickname (Optional[str]): The Mail nickname Example: PerformanceTest833.
        odata_type (Optional[str]): The Odata type Example: #microsoft.graph.group.
        on_premises_domain_name (Optional[str]): The On premises domain name Example: test.rpa.
        on_premises_net_bios_name (Optional[str]): The On premises net bios name Example: TEST.
        on_premises_sam_account_name (Optional[str]): The On premises sam account name Example: $F31000-RG52PIKBHDF3.
        proxy_addresses (Optional[list[str]]):
        renewed_date_time (Optional[datetime.datetime]): The Renewed date time Example: 2019-10-11T11:22:00Z.
        resource_behavior_options (Optional[list[str]]):
        resource_provisioning_options (Optional[list[str]]):
        role_template_id (Optional[str]): Unique identifier for the role template. Example:
                a9ea8996-122f-4c74-9520-8edcd192826c.
        security_enabled (Optional[bool]): The Security enabled Example: True.
        security_identifier (Optional[str]): The Security IDentifier Example:
                S-1-12-1-176064302-1264743275-3922293670-3676183120.
        visibility (Optional[str]): The Visibility Example: Private.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    creation_options: Optional[list[str]] = Field(alias="creationOptions", default=None)
    description: Optional[str] = Field(alias="description", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    expiration_date_time: Optional[datetime.datetime] = Field(
        alias="expirationDateTime", default=None
    )
    group_types: Optional[list[str]] = Field(alias="groupTypes", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    mail: Optional[str] = Field(alias="mail", default=None)
    mail_enabled: Optional[bool] = Field(alias="mailEnabled", default=None)
    mail_nickname: Optional[str] = Field(alias="mailNickname", default=None)
    odata_type: Optional[str] = Field(alias="odata_type", default=None)
    on_premises_domain_name: Optional[str] = Field(
        alias="onPremisesDomainName", default=None
    )
    on_premises_net_bios_name: Optional[str] = Field(
        alias="onPremisesNetBiosName", default=None
    )
    on_premises_sam_account_name: Optional[str] = Field(
        alias="onPremisesSamAccountName", default=None
    )
    proxy_addresses: Optional[list[str]] = Field(alias="proxyAddresses", default=None)
    renewed_date_time: Optional[datetime.datetime] = Field(
        alias="renewedDateTime", default=None
    )
    resource_behavior_options: Optional[list[str]] = Field(
        alias="resourceBehaviorOptions", default=None
    )
    resource_provisioning_options: Optional[list[str]] = Field(
        alias="resourceProvisioningOptions", default=None
    )
    role_template_id: Optional[str] = Field(alias="roleTemplateId", default=None)
    security_enabled: Optional[bool] = Field(alias="securityEnabled", default=None)
    security_identifier: Optional[str] = Field(alias="securityIdentifier", default=None)
    visibility: Optional[str] = Field(alias="visibility", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListAllGroupsOfAUser"], src_dict: Dict[str, Any]):
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
