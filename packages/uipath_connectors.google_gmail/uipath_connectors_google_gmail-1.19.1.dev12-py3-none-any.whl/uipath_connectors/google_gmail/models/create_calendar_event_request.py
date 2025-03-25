from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_calendar_event_request_show_as import (
    CreateCalendarEventRequestShowAs,
)
from ..models.create_calendar_event_request_visibility import (
    CreateCalendarEventRequestVisibility,
)
import datetime


class CreateCalendarEventRequest(BaseModel):
    """
    Attributes:
        end_date_time (datetime.datetime): Date time when event ends Example: 2023-01-02T06:35:28.631Z.
        event_title (str): The name of event Example: string.
        start_date_time (datetime.datetime): Date time when event starts Example: 2023-01-02T06:35:28.631Z.
        timezone (str): The timezone for event's start and end time Example: string.
        all_day_event (Optional[bool]):
        can_invite_others (Optional[bool]): Guests can invite others Default: True.
        can_modify_event (Optional[bool]): Guests can modify event
        can_see_attendees_list (Optional[bool]): Guests can see attendees Default: True.
        description (Optional[str]): The description of the event Example: string.
        location (Optional[str]): The location of the event Example: string.
        optional_attendees (Optional[str]): The comma separated list of optional attendees Example: string.
        output_event_timezone (Optional[str]): Timezone for output event. Example: string.
        required_attendees (Optional[str]): The comma separated list of required attendees Example: string.
        resource_attendees (Optional[str]): The comma separated list of resource attendees Example: string.
        show_as (Optional[CreateCalendarEventRequestShowAs]): Show as Default: CreateCalendarEventRequestShowAs.BUSY.
                Example: string.
        visibility (Optional[CreateCalendarEventRequestVisibility]): Visibility of the event. Default:
                CreateCalendarEventRequestVisibility.DEFAULT. Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    end_date_time: datetime.datetime = Field(alias="EndDateTime")
    event_title: str = Field(alias="EventTitle")
    start_date_time: datetime.datetime = Field(alias="StartDateTime")
    timezone: str = Field(alias="Timezone")
    all_day_event: Optional[bool] = Field(alias="AllDayEvent", default=None)
    can_invite_others: Optional[bool] = Field(alias="CanInviteOthers", default=True)
    can_modify_event: Optional[bool] = Field(alias="CanModifyEvent", default=None)
    can_see_attendees_list: Optional[bool] = Field(
        alias="CanSeeAttendeesList", default=True
    )
    description: Optional[str] = Field(alias="Description", default=None)
    location: Optional[str] = Field(alias="Location", default=None)
    optional_attendees: Optional[str] = Field(alias="OptionalAttendees", default=None)
    output_event_timezone: Optional[str] = Field(
        alias="OutputEventTimezone", default=None
    )
    required_attendees: Optional[str] = Field(alias="RequiredAttendees", default=None)
    resource_attendees: Optional[str] = Field(alias="ResourceAttendees", default=None)
    show_as: Optional["CreateCalendarEventRequestShowAs"] = Field(
        alias="ShowAs", default=CreateCalendarEventRequestShowAs.BUSY
    )
    visibility: Optional["CreateCalendarEventRequestVisibility"] = Field(
        alias="Visibility", default=CreateCalendarEventRequestVisibility.DEFAULT
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateCalendarEventRequest"], src_dict: Dict[str, Any]):
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
