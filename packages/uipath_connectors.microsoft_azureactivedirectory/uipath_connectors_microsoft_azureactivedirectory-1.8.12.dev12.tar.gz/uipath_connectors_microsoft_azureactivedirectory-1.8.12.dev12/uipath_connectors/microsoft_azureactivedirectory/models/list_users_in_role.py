from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class ListUsersInRole(BaseModel):
    """
    Attributes:
        business_phones (Optional[list[str]]):
        created_date_time (Optional[datetime.datetime]): The Created date time Example: 2023-10-26T13:00:39Z.
        display_name (Optional[str]): The Display name Example: Paul Ciobanu.
        given_name (Optional[str]): The Given name Example: Paul.
        id (Optional[str]): The ID Example: 01587839-4150-4f40-ace9-0b114e7d7f1e.
        is_assignable_to_role (Optional[bool]): The Is assignable to role Example: True.
        job_title (Optional[str]): The Job title Example: Sales Manager.
        mail (Optional[str]): The Mail Example: paul.ciobanu@uipathstaging.onmicrosoft.com.
        mail_enabled (Optional[bool]): The Mail enabled
        mail_nickname (Optional[str]): The Mail nickname Example: 74711eb1-3.
        mobile_phone (Optional[str]): The Mobile phone Example: +1 425 555 0100.
        odata_type (Optional[str]): The Odata type Example: #microsoft.graph.user.
        office_location (Optional[str]): The Office location Example: 18/2111345.
        preferred_language (Optional[str]): The Preferred language Example: en-US.
        renewed_date_time (Optional[datetime.datetime]): The Renewed date time Example: 2023-10-26T13:00:39Z.
        security_enabled (Optional[bool]): The Security enabled Example: True.
        security_identifier (Optional[str]): The Security IDentifier Example:
                S-1-12-1-1194015637-1195028599-2262917816-1130558578.
        surname (Optional[str]): The Surname Example: Ciobanu.
        user_principal_name (Optional[str]): The User principal name Example:
                paul.ciobanu@uipathstaging.onmicrosoft.com.
        visibility (Optional[str]): The Visibility Example: Private.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_phones: Optional[list[str]] = Field(alias="businessPhones", default=None)
    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    display_name: Optional[str] = Field(alias="displayName", default=None)
    given_name: Optional[str] = Field(alias="givenName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    is_assignable_to_role: Optional[bool] = Field(
        alias="isAssignableToRole", default=None
    )
    job_title: Optional[str] = Field(alias="jobTitle", default=None)
    mail: Optional[str] = Field(alias="mail", default=None)
    mail_enabled: Optional[bool] = Field(alias="mailEnabled", default=None)
    mail_nickname: Optional[str] = Field(alias="mailNickname", default=None)
    mobile_phone: Optional[str] = Field(alias="mobilePhone", default=None)
    odata_type: Optional[str] = Field(alias="odata_type", default=None)
    office_location: Optional[str] = Field(alias="officeLocation", default=None)
    preferred_language: Optional[str] = Field(alias="preferredLanguage", default=None)
    renewed_date_time: Optional[datetime.datetime] = Field(
        alias="renewedDateTime", default=None
    )
    security_enabled: Optional[bool] = Field(alias="securityEnabled", default=None)
    security_identifier: Optional[str] = Field(alias="securityIdentifier", default=None)
    surname: Optional[str] = Field(alias="surname", default=None)
    user_principal_name: Optional[str] = Field(alias="userPrincipalName", default=None)
    visibility: Optional[str] = Field(alias="visibility", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListUsersInRole"], src_dict: Dict[str, Any]):
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
