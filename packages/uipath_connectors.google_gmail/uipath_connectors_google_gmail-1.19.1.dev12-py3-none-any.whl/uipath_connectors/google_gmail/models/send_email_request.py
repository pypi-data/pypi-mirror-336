from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.send_email_request_importance import SendEmailRequestImportance


class SendEmailRequest(BaseModel):
    """
    Attributes:
        to (str): The primary recipients of the email, separated by comma (,) Example: string.
        bcc (Optional[str]): The hidden recipients of the email, separated by comma (,) Example: string.
        body (Optional[str]): The body of the email Example: string.
        cc (Optional[str]): The secondary recipients of the email, separated by comma (,) Example: string.
        importance (Optional[SendEmailRequestImportance]): The importance of the mail Default:
                SendEmailRequestImportance.NORMAL. Example: string.
        reply_to (Optional[str]): The email addresses to use when replying, separated by comma (,) Example: string.
        subject (Optional[str]): The subject of the email Example: string.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    to: str = Field(alias="To")
    bcc: Optional[str] = Field(alias="BCC", default=None)
    body: Optional[str] = Field(alias="Body", default=None)
    cc: Optional[str] = Field(alias="CC", default=None)
    importance: Optional["SendEmailRequestImportance"] = Field(
        alias="Importance", default=SendEmailRequestImportance.NORMAL
    )
    reply_to: Optional[str] = Field(alias="ReplyTo", default=None)
    subject: Optional[str] = Field(alias="Subject", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["SendEmailRequest"], src_dict: Dict[str, Any]):
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
