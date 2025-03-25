from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class AssignLicenseResponse(BaseModel):
    """
    Attributes:
        business_phones (Optional[list[str]]):
        display_name (Optional[str]): The full name displayed for the user. Example: John Doe.
        given_name (Optional[str]): The user's first name or given name. Example: John.
        id (Optional[str]): The unique identifier for the user. Example: b4e7abb3-fc22-4610-9c3b-28ae703b3bec.
        job_title (Optional[str]): The user's job title within the organization. Example: Sales Manager.
        mail (Optional[str]): The user's primary email address. Example: john.doe@contoso.com.
        mobile_phone (Optional[str]): The user's mobile phone number. Example: +1 425 555 0100.
        odata_context (Optional[str]): The Odata context Example:
                https://graph.microsoft.com/v1.0/$metadata#users/$entity.
        office_location (Optional[str]): The location of the user's office. Example: 18/2111345.
        preferred_language (Optional[str]): The user's preferred language for communication. Example: en-US.
        surname (Optional[str]): The last name of the user. Example: Sharma.
        user_principal_name (Optional[str]): The principal name used to identify the user. Example:
                7johndoe@uipathstaging.onmicrosoft.com.
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
    def from_dict(cls: Type["AssignLicenseResponse"], src_dict: Dict[str, Any]):
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
