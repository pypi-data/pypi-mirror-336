from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ApplyGmailLabelResponse(BaseModel):
    """
    Attributes:
        history_id (Optional[str]): Unique identifier for the change history of the email. Example: 99320.
        id (Optional[str]): A unique identifier for the email message. Example: 19488b1fa00ba1a8.
        internal_date (Optional[str]): The date and time when the email was received by Gmail. Example: 1737460152000.
        label_ids (Optional[list[str]]):
        size_estimate (Optional[int]): An estimate of the email message size in bytes. Example: 557.0.
        snippet (Optional[str]): A short preview of the email content.
        thread_id (Optional[str]): Unique identifier for the email thread. Example: 19488b1d21aed8cf.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    history_id: Optional[str] = Field(alias="historyId", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    internal_date: Optional[str] = Field(alias="internalDate", default=None)
    label_ids: Optional[list[str]] = Field(alias="labelIds", default=None)
    size_estimate: Optional[int] = Field(alias="sizeEstimate", default=None)
    snippet: Optional[str] = Field(alias="snippet", default=None)
    thread_id: Optional[str] = Field(alias="threadId", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ApplyGmailLabelResponse"], src_dict: Dict[str, Any]):
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
