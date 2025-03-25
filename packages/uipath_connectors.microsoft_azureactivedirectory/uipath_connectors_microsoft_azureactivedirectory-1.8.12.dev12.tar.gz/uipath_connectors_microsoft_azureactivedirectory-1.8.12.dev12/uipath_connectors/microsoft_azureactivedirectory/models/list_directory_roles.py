from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.list_directory_roles_value_array_item_ref import (
    ListDirectoryRolesValueArrayItemRef,
)


class ListDirectoryRoles(BaseModel):
    """
    Attributes:
        odata_context (Optional[str]): The Odata context Example:
                https://graph.microsoft.com/v1.0/$metadata#directoryRoles.
        value (Optional[list['ListDirectoryRolesValueArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    odata_context: Optional[str] = Field(alias="odata_context", default=None)
    value: Optional[list["ListDirectoryRolesValueArrayItemRef"]] = Field(
        alias="value", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ListDirectoryRoles"], src_dict: Dict[str, Any]):
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
