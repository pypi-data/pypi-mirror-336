from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class ForwardMailV2Request(BaseModel):
    """
    Attributes:
        to (str): The primary recipients of the email, separated by comma (,)
        bcc (Optional[str]): The hidden recipients of the email, separated by comma (,)
        body (Optional[str]): The body of the email
        cc (Optional[str]): The secondary recipients of the email, separated by comma (,)
        subject (Optional[str]): The new subject of the email. If left blank, the original subject is used
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    to: str = Field(alias="to")
    bcc: Optional[str] = Field(alias="bcc", default=None)
    body: Optional[str] = Field(alias="body", default=None)
    cc: Optional[str] = Field(alias="cc", default=None)
    subject: Optional[str] = Field(alias="subject", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["ForwardMailV2Request"], src_dict: Dict[str, Any]):
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
