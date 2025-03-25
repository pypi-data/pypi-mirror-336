from enum import Enum


class UpdateCalendarEventRequestChangeResourceAttendees(str, Enum):
    ADD_ANDOR_REMOVE = "addRemove"
    NO_CHANGE = "noChange"
    OVERWRITE = "overwrite"

    def __str__(self) -> str:
        return str(self.value)
