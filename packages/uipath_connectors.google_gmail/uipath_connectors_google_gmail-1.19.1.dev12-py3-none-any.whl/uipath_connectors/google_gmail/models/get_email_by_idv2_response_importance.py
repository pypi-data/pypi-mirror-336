from enum import Enum


class GetEmailByIDV2ResponseImportance(str, Enum):
    HIGH = "High"
    NORMAL = "Normal"

    def __str__(self) -> str:
        return str(self.value)
