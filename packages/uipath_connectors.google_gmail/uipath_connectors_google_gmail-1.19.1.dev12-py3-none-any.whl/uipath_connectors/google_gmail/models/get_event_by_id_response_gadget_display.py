from enum import Enum


class GetEventByIDResponseGadgetDisplay(str, Enum):
    CHIP = "chip"
    ICON = "icon"

    def __str__(self) -> str:
        return str(self.value)
