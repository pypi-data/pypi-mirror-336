from enum import Enum


class GetEventByIDResponseEventType(str, Enum):
    DEFAULT = "default"
    FOCUS_TIME = "focusTime"
    OUT_OF_OFFICE = "outOfOffice"

    def __str__(self) -> str:
        return str(self.value)
