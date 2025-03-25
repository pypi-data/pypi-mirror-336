from enum import Enum


class UpdateHostPoolResponseHostPoolType(str, Enum):
    PERSONAL = "Personal"
    POOLED = "Pooled"

    def __str__(self) -> str:
        return str(self.value)
