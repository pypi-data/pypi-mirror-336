from enum import Enum


class GetEmailByIDV2ResponseType(str, Enum):
    EMAIL = "email"

    def __str__(self) -> str:
        return str(self.value)
