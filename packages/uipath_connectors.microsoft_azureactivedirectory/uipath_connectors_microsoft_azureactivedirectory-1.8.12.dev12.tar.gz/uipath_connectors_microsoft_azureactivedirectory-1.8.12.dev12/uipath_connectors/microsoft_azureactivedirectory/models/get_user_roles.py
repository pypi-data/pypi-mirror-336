from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetUserRoles(BaseModel):
    """
    Attributes:
        description (Optional[str]): A brief description of the role. Example: Can manage all aspects of the Power BI
                product..
        display_name (Optional[str]): The name displayed for the role. Example: Power BI Administrator.
        id (Optional[str]): Unique identifier for the role. Example: 02c55166-f658-4a24-b222-b3080ee6b7ae.
        odata_type (Optional[str]): The Odata type Example: #microsoft.graph.directoryRole.
        role_template_id (Optional[str]): Unique identifier for the role template. Example:
                a9ea8996-122f-4c74-9520-8edcd192826c.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: Optional[str] = Field(alias="description", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    odata_type: Optional[str] = Field(alias="odata_type", default=None)
    role_template_id: Optional[str] = Field(alias="roleTemplateId", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetUserRoles"], src_dict: Dict[str, Any]):
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
