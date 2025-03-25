from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetUserResponse(BaseModel):
    """
    Attributes:
        account_enabled (Optional[bool]): Specifies if the user's account is enabled after creation. The default value
                is True. Example: True.
        business_phones (Optional[list[str]]):
        city (Optional[str]): The city where the user is located. Example: sf.
        company_name (Optional[str]): The name of the company or organization the user is associated with. Example:
                asdf.
        country (Optional[str]): The country where the user is located. Example: jhg.
        department (Optional[str]): The user's department. Example: sdf.
        display_name (Optional[str]): Establishes the display name of the user. This field supports only strings and
                String variables.
        given_name (Optional[str]): The user's first name Example: sdf.
        id (Optional[str]): A unique identifier assigned to the user. Example: 7853278c-81b6-4d68-a593-af34c9cfbe17.
        job_title (Optional[str]): The user's job title. Example: 15f1f995'2950'495f'bdfd'bab45cbac49e job title.
        legal_age_group_classification (Optional[str]): Classification of the user's legal age group for compliance.
                Example: Adult.
        mail (Optional[str]): The email address associated with the user. Example: john.doe@contoso.com.
        mail_nickname (Optional[str]): Specifies the mail alias of the user. This field supports only strings and String
                variables. Example: johndoe.
        mobile_phone (Optional[str]): The mobile phone number associated with the user. Example: +1 425 555 0100.
        office_location (Optional[str]): The physical location or address of the user's office. Example:
                1aa22111'd10a'400c'8a9a'aab4f22fd5d9 office location.
        on_premises_distinguished_name (Optional[str]): The distinguished name of the user in on-premises directory.
        on_premises_domain_name (Optional[str]): The domain name of the user's on-premises environment.
        on_premises_last_sync_date_time (Optional[str]): The date and time when the user last synced with on-premises.
        on_premises_sam_account_name (Optional[str]): The Security Account Manager account name used in the on-premises
                directory.
        on_premises_security_identifier (Optional[str]): A unique identifier for the user in the on-premises directory.
        on_premises_sync_enabled (Optional[str]): Indicates if the user is synchronized with the on-premises directory.
        on_premises_user_principal_name (Optional[str]): The user principal name used in the on-premises directory.
        postal_code (Optional[str]): The postal code of the user's address for location purposes. Example: jhg.
        preferred_language (Optional[str]): The language preferred by the user for communication. Example: en-US.
        state (Optional[str]): Indicates the current state or status of the user. Example: jhg.
        street_address (Optional[str]): The street address where the user is located. Example: asdf.
        surname (Optional[str]): The user's last name. Example: adsf.
        usage_location (Optional[str]): The country or region where the user primarily uses services. Example: US.
        user_principal_name (Optional[str]): Establishes the principal name of the user. This field supports only
                strings and String variables.
        user_type (Optional[str]): Specifies the type of user, such as member or guest. Example: Member.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account_enabled: Optional[bool] = Field(alias="accountEnabled", default=None)
    business_phones: Optional[list[str]] = Field(alias="businessPhones", default=None)
    city: Optional[str] = Field(alias="city", default=None)
    company_name: Optional[str] = Field(alias="companyName", default=None)
    country: Optional[str] = Field(alias="country", default=None)
    department: Optional[str] = Field(alias="department", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    given_name: Optional[str] = Field(alias="givenName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    job_title: Optional[str] = Field(alias="jobTitle", default=None)
    legal_age_group_classification: Optional[str] = Field(
        alias="legalAgeGroupClassification", default=None
    )
    mail: Optional[str] = Field(alias="mail", default=None)
    mail_nickname: Optional[str] = Field(alias="mailNickname", default=None)
    mobile_phone: Optional[str] = Field(alias="mobilePhone", default=None)
    office_location: Optional[str] = Field(alias="officeLocation", default=None)
    on_premises_distinguished_name: Optional[str] = Field(
        alias="onPremisesDistinguishedName", default=None
    )
    on_premises_domain_name: Optional[str] = Field(
        alias="onPremisesDomainName", default=None
    )
    on_premises_last_sync_date_time: Optional[str] = Field(
        alias="onPremisesLastSyncDateTime", default=None
    )
    on_premises_sam_account_name: Optional[str] = Field(
        alias="onPremisesSamAccountName", default=None
    )
    on_premises_security_identifier: Optional[str] = Field(
        alias="onPremisesSecurityIdentifier", default=None
    )
    on_premises_sync_enabled: Optional[str] = Field(
        alias="onPremisesSyncEnabled", default=None
    )
    on_premises_user_principal_name: Optional[str] = Field(
        alias="onPremisesUserPrincipalName", default=None
    )
    postal_code: Optional[str] = Field(alias="postalCode", default=None)
    preferred_language: Optional[str] = Field(alias="preferredLanguage", default=None)
    state: Optional[str] = Field(alias="state", default=None)
    street_address: Optional[str] = Field(alias="streetAddress", default=None)
    surname: Optional[str] = Field(alias="surname", default=None)
    usage_location: Optional[str] = Field(alias="usageLocation", default=None)
    user_principal_name: Optional[str] = Field(alias="userPrincipalName", default=None)
    user_type: Optional[str] = Field(alias="userType", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetUserResponse"], src_dict: Dict[str, Any]):
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
