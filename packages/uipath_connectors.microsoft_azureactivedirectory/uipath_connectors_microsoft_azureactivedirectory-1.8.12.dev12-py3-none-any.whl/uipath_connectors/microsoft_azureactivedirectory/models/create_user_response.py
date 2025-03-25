from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_user_response_password_profile import (
    CreateUserResponsePasswordProfile,
)


class CreateUserResponse(BaseModel):
    """
    Attributes:
        account_enabled (bool): Specifies if the user's account is enabled after creation. The default value is True.
                Example: True.
        display_name (str): Establishes the display name of the user. This field supports only strings and String
                variables.
        mail_nickname (str): Specifies the mail alias of the user. This field supports only strings and String
                variables. Example: johndoe.
        password_profile (Optional[CreateUserResponsePasswordProfile]):
        user_principal_name (str): Establishes the principal name of the user. This field supports only strings and
                String variables.
        given_name (Optional[str]): The user's first name Example: sdf.
        id (Optional[str]): A unique identifier assigned to the user. Example: 7853278c-81b6-4d68-a593-af34c9cfbe17.
        job_title (Optional[str]): The user's job title. Example: 15f1f995'2950'495f'bdfd'bab45cbac49e job title.
        odata_context (Optional[str]): URL providing context for the OData response structure. Example:
                https://graph.microsoft.com/v1.0/$metadata#users/$entity.
        surname (Optional[str]): The user's last name. Example: adsf.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account_enabled: bool = Field(alias="accountEnabled")
    display_name: str = Field(alias="displayName")
    mail_nickname: str = Field(alias="mailNickname")
    user_principal_name: str = Field(alias="userPrincipalName")
    password_profile: Optional["CreateUserResponsePasswordProfile"] = Field(
        alias="passwordProfile", default=None
    )
    given_name: Optional[str] = Field(alias="givenName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    job_title: Optional[str] = Field(alias="jobTitle", default=None)
    odata_context: Optional[str] = Field(alias="odata_context", default=None)
    surname: Optional[str] = Field(alias="surname", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateUserResponse"], src_dict: Dict[str, Any]):
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
