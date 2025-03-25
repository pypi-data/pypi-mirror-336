from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.update_calendar_event_request_change_optional_attendees import (
    UpdateCalendarEventRequestChangeOptionalAttendees,
)
from ..models.update_calendar_event_request_change_required_attendees import (
    UpdateCalendarEventRequestChangeRequiredAttendees,
)
from ..models.update_calendar_event_request_change_resource_attendees import (
    UpdateCalendarEventRequestChangeResourceAttendees,
)
from ..models.update_calendar_event_request_show_as import (
    UpdateCalendarEventRequestShowAs,
)
from ..models.update_calendar_event_request_visibility import (
    UpdateCalendarEventRequestVisibility,
)
import datetime


class UpdateCalendarEventRequest(BaseModel):
    """
    Attributes:
        all_day_event (Optional[bool]): Indicates if event takes place all day. This supersedes the Start and End time
                of the event. If left blank, the existing value will not be updated
        can_invite_others (Optional[bool]):
        can_modify_event (Optional[bool]):
        can_see_attendees_list (Optional[bool]):
        description (Optional[str]):  Example: string.
        end_date_time (Optional[datetime.datetime]): The new date and time for the end of the event. If left blank, the
                existing value will not be updated Example: 2023-01-02T06:35:28.631Z.
        event_title (Optional[str]): The new name of the event. If left blank, the existing value will not be updated
                Example: string.
        location (Optional[str]):  Example: string.
        optional_attendees (Optional[str]):  Example: string.
        output_event_timezone (Optional[str]):  Example: string.
        required_attendees (Optional[str]):  Example: string.
        resource_attendees (Optional[str]):  Example: string.
        show_as (Optional[UpdateCalendarEventRequestShowAs]): Show as Example: string.
        start_date_time (Optional[datetime.datetime]): The new date and time for the start of the event. If left blank,
                the existing value will not be updated Example: 2023-01-02T06:35:28.631Z.
        timezone (Optional[str]): The new timezone for the event. If left blank, the existing value will not be updated
                Example: string.
        visibility (Optional[UpdateCalendarEventRequestVisibility]): Visibility of the event. Example: string.
        add_optional_attendees (Optional[str]): Comma separated list of emails indicating the optional attendees to be
                added
        add_required_attendees (Optional[str]): Comma separated list of emails indicating the required attendees to be
                added Default: ''.
        add_resource_attendees (Optional[str]): Comma separated list of emails indicating the resource attendees to be
                added
        change_optional_attendees (Optional[UpdateCalendarEventRequestChangeOptionalAttendees]): Update the optional
                attended via one of the given option Default: UpdateCalendarEventRequestChangeOptionalAttendees.NO_CHANGE.
        change_required_attendees (Optional[UpdateCalendarEventRequestChangeRequiredAttendees]): Update the required
                attended via one of the given option Default: UpdateCalendarEventRequestChangeRequiredAttendees.NO_CHANGE.
        change_resource_attendees (Optional[UpdateCalendarEventRequestChangeResourceAttendees]): Update the resource
                attended via one of the given option Default: UpdateCalendarEventRequestChangeResourceAttendees.NO_CHANGE.
        remove_optional_attendees (Optional[str]): Comma separated list of emails indicating the optional attendees to
                be removed
        remove_required_attendees (Optional[str]): Comma separated list of emails indicating the required attendees to
                be removed
        remove_resource_attendees (Optional[str]): Comma separated list of emails indicating the resource attendees to
                be removed
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    all_day_event: Optional[bool] = Field(alias="AllDayEvent", default=None)
    can_invite_others: Optional[bool] = Field(alias="CanInviteOthers", default=None)
    can_modify_event: Optional[bool] = Field(alias="CanModifyEvent", default=None)
    can_see_attendees_list: Optional[bool] = Field(
        alias="CanSeeAttendeesList", default=None
    )
    description: Optional[str] = Field(alias="Description", default=None)
    end_date_time: Optional[datetime.datetime] = Field(
        alias="EndDateTime", default=None
    )
    event_title: Optional[str] = Field(alias="EventTitle", default=None)
    location: Optional[str] = Field(alias="Location", default=None)
    optional_attendees: Optional[str] = Field(alias="OptionalAttendees", default=None)
    output_event_timezone: Optional[str] = Field(
        alias="OutputEventTimezone", default=None
    )
    required_attendees: Optional[str] = Field(alias="RequiredAttendees", default=None)
    resource_attendees: Optional[str] = Field(alias="ResourceAttendees", default=None)
    show_as: Optional["UpdateCalendarEventRequestShowAs"] = Field(
        alias="ShowAs", default=None
    )
    start_date_time: Optional[datetime.datetime] = Field(
        alias="StartDateTime", default=None
    )
    timezone: Optional[str] = Field(alias="Timezone", default=None)
    visibility: Optional["UpdateCalendarEventRequestVisibility"] = Field(
        alias="Visibility", default=None
    )
    add_optional_attendees: Optional[str] = Field(
        alias="addOptionalAttendees", default=None
    )
    add_required_attendees: Optional[str] = Field(
        alias="addRequiredAttendees", default=""
    )
    add_resource_attendees: Optional[str] = Field(
        alias="addResourceAttendees", default=None
    )
    change_optional_attendees: Optional[
        "UpdateCalendarEventRequestChangeOptionalAttendees"
    ] = Field(
        alias="changeOptionalAttendees",
        default=UpdateCalendarEventRequestChangeOptionalAttendees.NO_CHANGE,
    )
    change_required_attendees: Optional[
        "UpdateCalendarEventRequestChangeRequiredAttendees"
    ] = Field(
        alias="changeRequiredAttendees",
        default=UpdateCalendarEventRequestChangeRequiredAttendees.NO_CHANGE,
    )
    change_resource_attendees: Optional[
        "UpdateCalendarEventRequestChangeResourceAttendees"
    ] = Field(
        alias="changeResourceAttendees",
        default=UpdateCalendarEventRequestChangeResourceAttendees.NO_CHANGE,
    )
    remove_optional_attendees: Optional[str] = Field(
        alias="removeOptionalAttendees", default=None
    )
    remove_required_attendees: Optional[str] = Field(
        alias="removeRequiredAttendees", default=None
    )
    remove_resource_attendees: Optional[str] = Field(
        alias="removeResourceAttendees", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["UpdateCalendarEventRequest"], src_dict: Dict[str, Any]):
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
