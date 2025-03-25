from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEmailByIDV2ResponseAttachmentsArrayItemRef(BaseModel):
    """
    Attributes:
        id (Optional[str]):  Example: id123.
        mime_type (Optional[str]):  Example: application/json.
        name (Optional[str]):  Example: workFile.
        size (Optional[int]):  Example: 256.
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
        cls: Type["GetEmailByIDV2ResponseAttachmentsArrayItemRef"],
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
