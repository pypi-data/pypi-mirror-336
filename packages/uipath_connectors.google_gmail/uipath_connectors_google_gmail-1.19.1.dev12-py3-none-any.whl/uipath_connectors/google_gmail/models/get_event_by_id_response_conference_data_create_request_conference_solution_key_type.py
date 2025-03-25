from enum import Enum


class GetEventByIDResponseConferenceDataCreateRequestConferenceSolutionKeyType(
    str, Enum
):
    ADD_ON = "addOn"
    EVENT_HANGOUT = "eventHangout"
    EVENT_NAMED_HANGOUT = "eventNamedHangout"
    HANGOUTS_MEET = "hangoutsMeet"

    def __str__(self) -> str:
        return str(self.value)
