from enum import Enum


class CreateHostPoolResponsePersonalDesktopAssignmentType(str, Enum):
    AUTOMATIC = "Automatic"
    DIRECT = "Direct"

    def __str__(self) -> str:
        return str(self.value)
