from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class GetEventByIDResponseOriginalStartTime(BaseModel):
    """
    Attributes:
        date (Optional[datetime.datetime]):  Example: 2022-04-28.
        date_time (Optional[datetime.datetime]):  Example: 2015-05-28T17:00:00-07:00.
        time_zone (Optional[str]):  Example: America/Los_Angeles.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    date: Optional[datetime.datetime] = Field(alias="date", default=None)
    date_time: Optional[datetime.datetime] = Field(alias="dateTime", default=None)
    time_zone: Optional[str] = Field(alias="timeZone", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEventByIDResponseOriginalStartTime"], src_dict: Dict[str, Any]
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
