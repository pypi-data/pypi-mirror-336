from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetGroupMembersDelta(BaseModel):
    """
    Attributes:
        group_id (Optional[str]): The unique identifier of the group in question Example:
                922af82c-51a2-4e03-8982-937606a570a9.
        id (Optional[str]): The unique identifier of the group member Example: 9fac4f6f-1c33-4971-b077-ae9ca5d67c03.
        object_type (Optional[str]): Specifies the type of the object, such as user or group Example:
                #microsoft.graph.user.
        removed (Optional[bool]): Indicates if a member was removed from the group Example: True.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    group_id: Optional[str] = Field(alias="groupId", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    object_type: Optional[str] = Field(alias="objectType", default=None)
    removed: Optional[bool] = Field(alias="removed", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetGroupMembersDelta"], src_dict: Dict[str, Any]):
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
