from enum import Enum


class CreateLifecyclePolicyRequestManagedGroupTypes(str, Enum):
    ALL = "All"
    NONE = "None"
    SELECTED = "Selected"

    def __str__(self) -> str:
        return str(self.value)
