from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class TurnOnAutomaticRepliesResponse(BaseModel):
    """
    Attributes:
        response_subject (str): The mail message subject used to be sent
        enable_auto_reply (Optional[bool]): Toggle to turn the automatic reply feature on or off.
        end_time (Optional[datetime.datetime]): Select when the Out of Office to be turned off. If the field is empty
                the Out of Office setting will be indefinitely Example: 1737527373.
        response_body_plain_text (Optional[str]): Insert the automatic replies message to be sent inside your
                organization. If the field is empty the message set in Gmail settings is going to be used
        restrict_to_contacts (Optional[bool]): Set if the automatic replies for users outside the organization can be
                sent only to contacts
        restrict_to_domain (Optional[bool]): Set if the automatic replies can be sent outside user organization
        start_time (Optional[datetime.datetime]): Select when the Out of Office to be turned on. If the field is empty
                the Out of Office setting will be turned on immediately Example: 1737527373.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    response_subject: str = Field(alias="responseSubject")
    enable_auto_reply: Optional[bool] = Field(alias="enableAutoReply", default=None)
    end_time: Optional[datetime.datetime] = Field(alias="endTime", default=None)
    response_body_plain_text: Optional[str] = Field(
        alias="responseBodyPlainText", default=None
    )
    restrict_to_contacts: Optional[bool] = Field(
        alias="restrictToContacts", default=None
    )
    restrict_to_domain: Optional[bool] = Field(alias="restrictToDomain", default=None)
    start_time: Optional[datetime.datetime] = Field(alias="startTime", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["TurnOnAutomaticRepliesResponse"], src_dict: Dict[str, Any]
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
