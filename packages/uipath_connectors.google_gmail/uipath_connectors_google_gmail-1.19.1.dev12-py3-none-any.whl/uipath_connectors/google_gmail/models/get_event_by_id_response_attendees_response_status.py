from enum import Enum


class GetEventByIDResponseAttendeesResponseStatus(str, Enum):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    NEEDS_ACTION = "needsAction"
    TENTATIVE = "tentative"

    def __str__(self) -> str:
        return str(self.value)
