from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListUsersInGroup(BaseModel):
    """
    Attributes:
        display_name (Optional[str]): The name displayed for the user in the directory. Example: insightspgov.
        given_name (Optional[str]): The Given name Example: Kshitij.
        id (Optional[str]): A unique identifier assigned to the user. Example: ee021468-10c3-4454-8503-83976dde3566.
        job_title (Optional[str]): The Job title Example: Cloud Engineer.
        mail (Optional[str]): The email address associated with the user. Example:
                devuser3@uipathstaging.onmicrosoft.com.
        odata_type (Optional[str]): The Odata type Example: #microsoft.graph.user.
        surname (Optional[str]): The Surname Example: Sharma.
        user_principal_name (Optional[str]): The principal name used to identify the user. Example:
                insightspgov@uipathstaging.onmicrosoft.com.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display_name: Optional[str] = Field(alias="displayName", default=None)
    given_name: Optional[str] = Field(alias="givenName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    job_title: Optional[str] = Field(alias="jobTitle", default=None)
    mail: Optional[str] = Field(alias="mail", default=None)
    odata_type: Optional[str] = Field(alias="odata_type", default=None)
    surname: Optional[str] = Field(alias="surname", default=None)
    user_principal_name: Optional[str] = Field(alias="userPrincipalName", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListUsersInGroup"], src_dict: Dict[str, Any]):
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
