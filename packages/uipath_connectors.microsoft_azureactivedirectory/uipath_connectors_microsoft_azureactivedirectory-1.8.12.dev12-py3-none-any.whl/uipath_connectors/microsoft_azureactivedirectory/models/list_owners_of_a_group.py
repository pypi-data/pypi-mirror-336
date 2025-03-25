from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ListOwnersOfAGroup(BaseModel):
    """
    Attributes:
        display_name (Optional[str]): The name shown for the user or group. Example: Kshitij Sharma.
        given_name (Optional[str]): The first name of the user. Example: Kshitij.
        id (Optional[str]): A unique identifier for the user or group. Example: abddd7a4-c0d4-45bf-817e-993a6760c79d.
        odata_type (Optional[str]): The Odata type Example: #microsoft.graph.user.
        surname (Optional[str]): The last name of the user. Example: Sharma.
        user_principal_name (Optional[str]): The unique identifier for a user in email format. Example:
                kshitij.sharma0964@uipathstaging.onmicrosoft.com.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display_name: Optional[str] = Field(alias="displayName", default=None)
    given_name: Optional[str] = Field(alias="givenName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    odata_type: Optional[str] = Field(alias="odata_type", default=None)
    surname: Optional[str] = Field(alias="surname", default=None)
    user_principal_name: Optional[str] = Field(alias="userPrincipalName", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListOwnersOfAGroup"], src_dict: Dict[str, Any]):
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
