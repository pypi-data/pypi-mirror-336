from enum import Enum


class RespondToEventInvitationRequestResponse(str, Enum):
    ACCEPT = "accepted"
    DECLINE = "declined"
    TENTATIVELY_ACCEPT = "tentative"

    def __str__(self) -> str:
        return str(self.value)
