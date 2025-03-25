from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_event_by_id_response_attendees_response_status import (
    GetEventByIDResponseAttendeesResponseStatus,
)


class GetEventByIDResponseAttendeesArrayItemRef(BaseModel):
    """
    Attributes:
        additional_guests (Optional[int]):  Example: 2.0.
        comment (Optional[str]):  Example: string.
        display_name (Optional[str]):  Example: string.
        email (Optional[str]):  Example: lpage@example.com.
        id (Optional[str]):  Example: 1122213.
        optional (Optional[bool]):  Example: True.
        organizer (Optional[bool]):  Example: True.
        resource (Optional[bool]):  Example: True.
        response_status (Optional[GetEventByIDResponseAttendeesResponseStatus]):  Example: needsAction.
        self_ (Optional[bool]):  Example: True.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    additional_guests: Optional[int] = Field(alias="additionalGuests", default=None)
    comment: Optional[str] = Field(alias="comment", default=None)
    display_name: Optional[str] = Field(alias="displayName", default=None)
    email: Optional[str] = Field(alias="email", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    optional: Optional[bool] = Field(alias="optional", default=None)
    organizer: Optional[bool] = Field(alias="organizer", default=None)
    resource: Optional[bool] = Field(alias="resource", default=None)
    response_status: Optional["GetEventByIDResponseAttendeesResponseStatus"] = Field(
        alias="responseStatus", default=None
    )
    self_: Optional[bool] = Field(alias="self", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEventByIDResponseAttendeesArrayItemRef"], src_dict: Dict[str, Any]
    ):
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
