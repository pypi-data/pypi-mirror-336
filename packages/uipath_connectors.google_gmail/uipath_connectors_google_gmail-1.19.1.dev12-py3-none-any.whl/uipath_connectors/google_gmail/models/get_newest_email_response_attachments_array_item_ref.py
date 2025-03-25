from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetNewestEmailResponseAttachmentsArrayItemRef(BaseModel):
    """
    Attributes:
        id (Optional[str]): Unique identifier for each attachment in the email. Example: ANGjdJ_ANkWFd_YpksXwXK_vfLyrZ8f
                jGlB6_yOpH4O0Y6_JlHefaEIPPKFIZncU9k5v4RmDTgsD60eaHSD6wpizf0Rc47BugG33lmGs9YoECZWqHjX3GPN7cBXsV3zuTKlnFlju3xI5K4a
                iZ19sIeEV3jDlW7sk_8eVwmcRlXHclwE9NQfd4K1r7-
                L2Ij1nXhnEUCZ3TooyulE5w8e8RCrrbWa340LVI0yRMyV3TwOj6PrFOFcRdR3qIZ86b8bcWuFdS1DMqDWPJUHcA367SJ_DO64Tq_grl64dLk_f5N
                AstenkG4rr6mdIzIq0NMrXQF3DRLGGassS0xVRkN6Zk7QscoDAO0bK3d4HgMi0c2RuDr8RgkqwBLyg6CWIljzlWuAliIjRNxlZy_XeNo01.
        mime_type (Optional[str]): Specifies the MIME type of each attachment in the email. Example: application/json.
        name (Optional[str]): The name of the file attached to the email. Example: bindings_v2.json.
        size (Optional[int]): The size of each attachment in the email. Example: 1081.0.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: Optional[str] = Field(alias="ID", default=None)
    mime_type: Optional[str] = Field(alias="MIMEType", default=None)
    name: Optional[str] = Field(alias="Name", default=None)
    size: Optional[int] = Field(alias="Size", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetNewestEmailResponseAttachmentsArrayItemRef"],
        src_dict: Dict[str, Any],
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
