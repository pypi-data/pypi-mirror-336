from enum import Enum


class UpdateCalendarEventRequestChangeOptionalAttendees(str, Enum):
    ADD_ANDOR_REMOVE = "addRemove"
    NO_CHANGE = "noChange"
    OVERWRITE = "overwrite"

    def __str__(self) -> str:
        return str(self.value)
