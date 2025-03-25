from enum import Enum


class GetEventByIDResponseRemindersOverridesMethod(str, Enum):
    EMAIL = "email"
    POPUP = "popup"

    def __str__(self) -> str:
        return str(self.value)
