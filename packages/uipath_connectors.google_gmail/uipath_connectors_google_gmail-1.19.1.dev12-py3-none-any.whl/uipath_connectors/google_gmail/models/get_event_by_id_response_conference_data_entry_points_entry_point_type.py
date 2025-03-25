from enum import Enum


class GetEventByIDResponseConferenceDataEntryPointsEntryPointType(str, Enum):
    MORE = "more"
    PHONE = "phone"
    SIP = "sip"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
