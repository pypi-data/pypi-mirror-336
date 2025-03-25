from enum import Enum


class ListsLifecyclePolicyManagedGroupTypes(str, Enum):
    ALL = "All"
    NONE = "None"
    SELECTED = "Selected"

    def __str__(self) -> str:
        return str(self.value)
