from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_event_by_id_response_attachments_array_item_ref import (
    GetEventByIDResponseAttachmentsArrayItemRef,
)
from ..models.get_event_by_id_response_attendees_array_item_ref import (
    GetEventByIDResponseAttendeesArrayItemRef,
)
from ..models.get_event_by_id_response_conference_data import (
    GetEventByIDResponseConferenceData,
)
from ..models.get_event_by_id_response_creator import GetEventByIDResponseCreator
from ..models.get_event_by_id_response_end import GetEventByIDResponseEnd
from ..models.get_event_by_id_response_event_type import GetEventByIDResponseEventType
from ..models.get_event_by_id_response_gadget import GetEventByIDResponseGadget
from ..models.get_event_by_id_response_organizer import GetEventByIDResponseOrganizer
from ..models.get_event_by_id_response_original_start_time import (
    GetEventByIDResponseOriginalStartTime,
)
from ..models.get_event_by_id_response_reminders import GetEventByIDResponseReminders
from ..models.get_event_by_id_response_source import GetEventByIDResponseSource
from ..models.get_event_by_id_response_start import GetEventByIDResponseStart
from ..models.get_event_by_id_response_status import GetEventByIDResponseStatus
from ..models.get_event_by_id_response_transparency import (
    GetEventByIDResponseTransparency,
)
from ..models.get_event_by_id_response_visibility import GetEventByIDResponseVisibility
import datetime


class GetEventByIDResponse(BaseModel):
    """
    Attributes:
        anyone_can_add_self (Optional[bool]):
        attachments (Optional[list['GetEventByIDResponseAttachmentsArrayItemRef']]):
        attendees (Optional[list['GetEventByIDResponseAttendeesArrayItemRef']]):
        attendees_omitted (Optional[bool]):
        color_id (Optional[str]):  Example: 1.
        conference_data (Optional[GetEventByIDResponseConferenceData]):
        created (Optional[datetime.datetime]):  Example: 2022-03-15T09:07:55.000Z.
        creator (Optional[GetEventByIDResponseCreator]):
        description (Optional[str]):  Example: description.
        end (Optional[GetEventByIDResponseEnd]):
        end_time_unspecified (Optional[bool]):
        etag (Optional[str]):  Example: "3294670552197000".
        event_type (Optional[GetEventByIDResponseEventType]):  Example: default.
        gadget (Optional[GetEventByIDResponseGadget]):
        guests_can_invite_others (Optional[bool]):
        guests_can_modify (Optional[bool]):
        guests_can_see_other_guests (Optional[bool]):
        hangout_link (Optional[str]):  Example: https://www.google.com/calendar/event?eid=NDAzbDRkNmJwZWFkaTNidDhzcGxidG
                o0bzhfMjAxNTA1MjhUMTYwMDAwWiB2dG00a2R0NWx0bWxkb2QzbnFtbTVpdW80NEBn.
        html_link (Optional[str]):  Example: https://www.google.com/calendar/event?eid=NDAzbDRkNmJwZWFkaTNidDhzcGxidGo0b
                zhfMjAxNTA1MjhUMTYwMDAwWiB2dG00a2R0NWx0bWxkb2QzbnFtbTVpdW80NEBn.
        i_cal_uid (Optional[str]):  Example: p4p4rdhrf1jq4mrn07ska4hqrs@google.com.
        id (Optional[str]):  Example: 403l4d6bpeadi3bt8splbtj4o8.
        kind (Optional[str]):  Example: calendar#event.
        location (Optional[str]):  Example: 800 Howard St., San Francisco, CA 94103.
        locked (Optional[bool]):
        organizer (Optional[GetEventByIDResponseOrganizer]):
        original_start_time (Optional[GetEventByIDResponseOriginalStartTime]):
        private_copy (Optional[bool]):
        recurrence (Optional[list[str]]):
        recurring_event_id (Optional[str]):  Example: string.
        reminders (Optional[GetEventByIDResponseReminders]):
        sequence (Optional[int]):  Example: 1.0.
        source (Optional[GetEventByIDResponseSource]):
        start (Optional[GetEventByIDResponseStart]):
        status (Optional[GetEventByIDResponseStatus]):  Example: confirmed.
        summary (Optional[str]):  Example: summary.
        transparency (Optional[GetEventByIDResponseTransparency]):  Example: string.
        updated (Optional[datetime.datetime]):  Example: 2022-03-15T09:07:56.186Z.
        visibility (Optional[GetEventByIDResponseVisibility]):  Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    anyone_can_add_self: Optional[bool] = Field(alias="anyoneCanAddSelf", default=None)
    attachments: Optional[list["GetEventByIDResponseAttachmentsArrayItemRef"]] = Field(
        alias="attachments", default=None
    )
    attendees: Optional[list["GetEventByIDResponseAttendeesArrayItemRef"]] = Field(
        alias="attendees", default=None
    )
    attendees_omitted: Optional[bool] = Field(alias="attendeesOmitted", default=None)
    color_id: Optional[str] = Field(alias="colorId", default=None)
    conference_data: Optional["GetEventByIDResponseConferenceData"] = Field(
        alias="conferenceData", default=None
    )
    created: Optional[datetime.datetime] = Field(alias="created", default=None)
    creator: Optional["GetEventByIDResponseCreator"] = Field(
        alias="creator", default=None
    )
    description: Optional[str] = Field(alias="description", default=None)
    end: Optional["GetEventByIDResponseEnd"] = Field(alias="end", default=None)
    end_time_unspecified: Optional[bool] = Field(
        alias="endTimeUnspecified", default=None
    )
    etag: Optional[str] = Field(alias="etag", default=None)
    event_type: Optional["GetEventByIDResponseEventType"] = Field(
        alias="eventType", default=None
    )
    gadget: Optional["GetEventByIDResponseGadget"] = Field(alias="gadget", default=None)
    guests_can_invite_others: Optional[bool] = Field(
        alias="guestsCanInviteOthers", default=None
    )
    guests_can_modify: Optional[bool] = Field(alias="guestsCanModify", default=None)
    guests_can_see_other_guests: Optional[bool] = Field(
        alias="guestsCanSeeOtherGuests", default=None
    )
    hangout_link: Optional[str] = Field(alias="hangoutLink", default=None)
    html_link: Optional[str] = Field(alias="htmlLink", default=None)
    i_cal_uid: Optional[str] = Field(alias="iCalUID", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    kind: Optional[str] = Field(alias="kind", default=None)
    location: Optional[str] = Field(alias="location", default=None)
    locked: Optional[bool] = Field(alias="locked", default=None)
    organizer: Optional["GetEventByIDResponseOrganizer"] = Field(
        alias="organizer", default=None
    )
    original_start_time: Optional["GetEventByIDResponseOriginalStartTime"] = Field(
        alias="originalStartTime", default=None
    )
    private_copy: Optional[bool] = Field(alias="privateCopy", default=None)
    recurrence: Optional[list[str]] = Field(alias="recurrence", default=None)
    recurring_event_id: Optional[str] = Field(alias="recurringEventId", default=None)
    reminders: Optional["GetEventByIDResponseReminders"] = Field(
        alias="reminders", default=None
    )
    sequence: Optional[int] = Field(alias="sequence", default=None)
    source: Optional["GetEventByIDResponseSource"] = Field(alias="source", default=None)
    start: Optional["GetEventByIDResponseStart"] = Field(alias="start", default=None)
    status: Optional["GetEventByIDResponseStatus"] = Field(alias="status", default=None)
    summary: Optional[str] = Field(alias="summary", default=None)
    transparency: Optional["GetEventByIDResponseTransparency"] = Field(
        alias="transparency", default=None
    )
    updated: Optional[datetime.datetime] = Field(alias="updated", default=None)
    visibility: Optional["GetEventByIDResponseVisibility"] = Field(
        alias="visibility", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEventByIDResponse"], src_dict: Dict[str, Any]):
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
