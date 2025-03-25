from enum import Enum


class GetEventByIDResponseStatus(str, Enum):
    CANCELLED = "cancelled"
    CONFIRMED = "confirmed"
    TENTATIVE = "tentative"

    def __str__(self) -> str:
        return str(self.value)
