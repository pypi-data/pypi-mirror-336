from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_event_by_id_response_gadget_display import (
    GetEventByIDResponseGadgetDisplay,
)


class GetEventByIDResponseGadget(BaseModel):
    """
    Attributes:
        display (Optional[GetEventByIDResponseGadgetDisplay]):  Example: string.
        height (Optional[int]):  Example: 12.0.
        icon_link (Optional[str]):  Example: string.
        link (Optional[str]):  Example: string.
        title (Optional[str]):  Example: string.
        type_ (Optional[str]):  Example: string.
        width (Optional[int]):  Example: 12.0.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    display: Optional["GetEventByIDResponseGadgetDisplay"] = Field(
        alias="display", default=None
    )
    height: Optional[int] = Field(alias="height", default=None)
    icon_link: Optional[str] = Field(alias="iconLink", default=None)
    link: Optional[str] = Field(alias="link", default=None)
    title: Optional[str] = Field(alias="title", default=None)
    type_: Optional[str] = Field(alias="type", default=None)
    width: Optional[int] = Field(alias="width", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEventByIDResponseGadget"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
