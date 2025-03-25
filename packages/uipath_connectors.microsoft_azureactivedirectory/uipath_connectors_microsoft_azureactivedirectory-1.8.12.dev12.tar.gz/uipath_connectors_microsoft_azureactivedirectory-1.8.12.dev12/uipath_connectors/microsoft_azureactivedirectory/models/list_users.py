from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListUsers(BaseModel):
    """
    Attributes:
        business_phones (Optional[list[str]]):
        display_name (Optional[str]): Establishes the display name of the user. This field supports only strings and
                String variables.
        given_name (Optional[str]): The user's first name Example: sdf.
        id (Optional[str]): A unique identifier assigned to the user. Example: 7853278c-81b6-4d68-a593-af34c9cfbe17.
        job_title (Optional[str]): The user's job title. Example: 15f1f995'2950'495f'bdfd'bab45cbac49e job title.
        mail (Optional[str]): The email address associated with the user. Example: john.doe@contoso.com.
        mobile_phone (Optional[str]): The mobile phone number associated with the user. Example: +1 425 555 0100.
        odata_context (Optional[str]): URL providing context for the OData response structure. Example:
                https://graph.microsoft.com/v1.0/$metadata#users/$entity.
        office_location (Optional[str]): The physical location or address of the user's office. Example:
                1aa22111'd10a'400c'8a9a'aab4f22fd5d9 office location.
        preferred_language (Optional[str]): The language preferred by the user for communication. Example: en-US.
        surname (Optional[str]): The user's last name. Example: adsf.
        user_principal_name (Optional[str]): Establishes the principal name of the user. This field supports only
                strings and String variables.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    business_phones: Optional[list[str]] = Field(alias="businessPhones", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    given_name: Optional[str] = Field(alias="givenName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    job_title: Optional[str] = Field(alias="jobTitle", default=None)
    mail: Optional[str] = Field(alias="mail", default=None)
    mobile_phone: Optional[str] = Field(alias="mobilePhone", default=None)
    odata_context: Optional[str] = Field(alias="odata_context", default=None)
    office_location: Optional[str] = Field(alias="officeLocation", default=None)
    preferred_language: Optional[str] = Field(alias="preferredLanguage", default=None)
    surname: Optional[str] = Field(alias="surname", default=None)
    user_principal_name: Optional[str] = Field(alias="userPrincipalName", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListUsers"], src_dict: Dict[str, Any]):
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
