from enum import Enum


class GetHostPoolResponsePersonalDesktopAssignmentType(str, Enum):
    AUTOMATIC = "Automatic"
    DIRECT = "Direct"

    def __str__(self) -> str:
        return str(self.value)
