from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.respond_to_event_invitation_request_response import (
    RespondToEventInvitationRequestResponse,
)


class RespondToEventInvitationRequest(BaseModel):
    """
    Attributes:
        response (RespondToEventInvitationRequestResponse): The response sent to event organizer Default:
                RespondToEventInvitationRequestResponse.ACCEPT.
        additional_guests (Optional[int]): The number of additional guests
        comment (Optional[str]): The note sent along the response. Comment is not sent when 'Send response notification'
                is disabled.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    response: "RespondToEventInvitationRequestResponse" = Field(
        alias="response", default=RespondToEventInvitationRequestResponse.ACCEPT
    )
    additional_guests: Optional[int] = Field(alias="additionalGuests", default=None)
    comment: Optional[str] = Field(alias="comment", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["RespondToEventInvitationRequest"], src_dict: Dict[str, Any]
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
