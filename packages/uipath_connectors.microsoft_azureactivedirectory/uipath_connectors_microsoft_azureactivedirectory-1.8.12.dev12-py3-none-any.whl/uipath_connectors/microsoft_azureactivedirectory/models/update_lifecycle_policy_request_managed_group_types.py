from enum import Enum


class UpdateLifecyclePolicyRequestManagedGroupTypes(str, Enum):
    ALL = "All"
    NONE = "None"
    SELECTED = "Selected"

    def __str__(self) -> str:
        return str(self.value)
