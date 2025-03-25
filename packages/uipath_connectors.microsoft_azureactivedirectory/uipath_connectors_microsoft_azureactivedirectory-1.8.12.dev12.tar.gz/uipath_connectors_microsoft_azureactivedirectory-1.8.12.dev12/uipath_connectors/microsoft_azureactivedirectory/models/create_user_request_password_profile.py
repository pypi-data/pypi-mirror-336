from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Type



class CreateUserRequestPasswordProfile(BaseModel):
    """
    Attributes:
        force_change_password_next_sign_in (bool): Specifies if the change password action should be forced on the next
                login. The default value is False. Default: False.
        force_change_password_next_sign_in_with_mfa (bool): Specifies if a multi-factor authentication (MFA) should be
                done before the change password action that was forced on the next login. The default value is False. Default:
                False.
        password (str): Specifies the initial password of the user. Example: xWwvJ]6NMw+bWH-d.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    password: str = Field(alias="password")
    force_change_password_next_sign_in: bool = Field(
        alias="forceChangePasswordNextSignIn", default=False
    )
    force_change_password_next_sign_in_with_mfa: bool = Field(
        alias="forceChangePasswordNextSignInWithMfa", default=False
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["CreateUserRequestPasswordProfile"], src_dict: Dict[str, Any]
    ):
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
