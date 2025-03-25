from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class CreateAssignedGroupResponse(BaseModel):
    """
    Attributes:
        display_name (str): The display name of the group. Example: apitest2e83bfb3-7391-4b20-a125-a84ba7a718a4.
        mail_enabled (bool): Specifies whether the group is mail-enabled.
        mail_nickname (str): The mail alias for the group. Example: ahwexusaiwarxk.
        security_enabled (bool): Specifies whether the group is a security group. Example: True.
        created_date_time (Optional[datetime.datetime]): The date and time when the group was created. Example:
                2023-10-02T06:15:32Z.
        description (Optional[str]): The description of the group. Example: o365_test_group_temp desc.
        id (Optional[str]): A unique identifier for the group. Example: 000f1dde-b510-4a50-801e-07d77e06f535.
        renewed_date_time (Optional[datetime.datetime]): The date and time when the group was last renewed. Example:
                2023-10-02T06:15:32Z.
        security_identifier (Optional[str]): A unique identifier for the group used for security purposes. Example:
                S-1-12-1-990686-1246803216-3607568000-905250430.
        visibility (Optional[str]): The visibility of the group. Example: Public.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display_name: str = Field(alias="displayName")
    mail_enabled: bool = Field(alias="mailEnabled")
    mail_nickname: str = Field(alias="mailNickname")
    security_enabled: bool = Field(alias="securityEnabled")
    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    description: Optional[str] = Field(alias="description", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    renewed_date_time: Optional[datetime.datetime] = Field(
        alias="renewedDateTime", default=None
    )
    security_identifier: Optional[str] = Field(alias="securityIdentifier", default=None)
    visibility: Optional[str] = Field(alias="visibility", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateAssignedGroupResponse"], src_dict: Dict[str, Any]):
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
