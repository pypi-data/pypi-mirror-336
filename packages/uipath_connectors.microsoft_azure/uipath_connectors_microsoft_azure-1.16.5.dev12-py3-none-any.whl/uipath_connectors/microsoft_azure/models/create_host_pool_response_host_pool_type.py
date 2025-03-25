from enum import Enum


class CreateHostPoolResponseHostPoolType(str, Enum):
    PERSONAL = "Personal"
    POOLED = "Pooled"

    def __str__(self) -> str:
        return str(self.value)
