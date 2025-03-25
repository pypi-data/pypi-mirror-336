from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class GetGroupByIdResponse(BaseModel):
    """
    Attributes:
        classification (Optional[str]): A label that categorizes the group for organizational purposes. Example:
                General.
        created_date_time (Optional[datetime.datetime]): The date and time when the group was created. Example:
                2023-10-02T06:15:32Z.
        deleted_date_time (Optional[datetime.datetime]): The date and time when the group was deleted. Example:
                1970-01-01T00:00:00Z.
        description (Optional[str]): The description of the group. Example: o365_test_group_temp desc.
        display_name (Optional[str]): The display name of the group. Example:
                apitest2e83bfb3-7391-4b20-a125-a84ba7a718a4.
        expiration_date_time (Optional[datetime.datetime]): The date and time when the group will expire. Example:
                1970-01-01T00:00:00Z.
        id (Optional[str]): A unique identifier for the group. Example: 000f1dde-b510-4a50-801e-07d77e06f535.
        is_assignable_to_role (Optional[bool]): Indicates if the group can be assigned to a role.
        mail (Optional[str]): The email address associated with the group. Example:
                o365_test_group_temp_YAID5@uipathstaging.onmicrosoft.com.
        mail_enabled (Optional[bool]): Specifies whether the group is mail-enabled.
        mail_nickname (Optional[str]): The mail alias for the group. Example: ahwexusaiwarxk.
        membership_rule (Optional[str]): The rule that defines the membership criteria for the group.
        membership_rule_processing_state (Optional[str]): The current processing state of the membership rule. Example:
                NotProcessing.
        odata_context (Optional[str]): Provides context about the OData response, including metadata. Example:
                https://graph.microsoft.com/v1.0/$metadata#groups/$entity.
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
        preferred_data_location (Optional[str]): The desired geographic location for storing the group's data. Example:
                global.
        preferred_language (Optional[str]): The language preference set for the group. Example: en-US.
        renewed_date_time (Optional[datetime.datetime]): The date and time when the group was last renewed. Example:
                2023-10-02T06:15:32Z.
        security_enabled (Optional[bool]): Specifies whether the group is a security group. Example: True.
        security_identifier (Optional[str]): A unique identifier for the group used for security purposes. Example:
                S-1-12-1-990686-1246803216-3607568000-905250430.
        theme (Optional[str]): Specifies the theme or visual style associated with the group. Example: default.
        unique_name (Optional[str]): A distinct name that identifies the group within the directory.
        visibility (Optional[str]): The visibility of the group. Example: Public.
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
    odata_context: Optional[str] = Field(alias="odata_context", default=None)
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
    def from_dict(cls: Type["GetGroupByIdResponse"], src_dict: Dict[str, Any]):
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
