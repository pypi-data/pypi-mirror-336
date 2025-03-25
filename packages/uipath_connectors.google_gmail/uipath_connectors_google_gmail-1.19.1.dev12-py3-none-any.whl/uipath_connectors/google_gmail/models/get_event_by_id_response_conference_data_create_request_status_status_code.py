from enum import Enum


class GetEventByIDResponseConferenceDataCreateRequestStatusStatusCode(str, Enum):
    FAILURE = "failure"
    PENDING = "pending"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
