from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_newest_email_response_attachments_array_item_ref import (
    GetNewestEmailResponseAttachmentsArrayItemRef,
)
from ..models.get_newest_email_response_categories_array_item_ref import (
    GetNewestEmailResponseCategoriesArrayItemRef,
)
from ..models.get_newest_email_response_from import GetNewestEmailResponseFrom
from ..models.get_newest_email_response_parent_folders_array_item_ref import (
    GetNewestEmailResponseParentFoldersArrayItemRef,
)
from ..models.get_newest_email_response_to_array_item_ref import (
    GetNewestEmailResponseToArrayItemRef,
)


class GetNewestEmailResponse(BaseModel):
    """
    Attributes:
        attachments (Optional[list['GetNewestEmailResponseAttachmentsArrayItemRef']]):
        body (Optional[str]): The main content of the email message. Example: Body of v2 email.
        categories (Optional[list['GetNewestEmailResponseCategoriesArrayItemRef']]):
        from_ (Optional[GetNewestEmailResponseFrom]):
        has_attachments (Optional[bool]): Indicates whether the email contains any attachments. Example: True.
        id (Optional[str]): The unique identifier for the email. Example: 195c76f3342acfe7.
        importance (Optional[str]): Indicates the priority or significance of the email. Example: Normal.
        parent_folders (Optional[list['GetNewestEmailResponseParentFoldersArrayItemRef']]):
        subject (Optional[str]): The subject line of the email message. Example: Test send email V2.
        thread_id (Optional[str]): A unique identifier for the email thread. Example: 195c76f3342acfe7.
        to (Optional[list['GetNewestEmailResponseToArrayItemRef']]):
        type_ (Optional[str]): Specifies the category or format of the email. Example: email.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attachments: Optional[list["GetNewestEmailResponseAttachmentsArrayItemRef"]] = (
        Field(alias="Attachments", default=None)
    )
    body: Optional[str] = Field(alias="Body", default=None)
    categories: Optional[list["GetNewestEmailResponseCategoriesArrayItemRef"]] = Field(
        alias="Categories", default=None
    )
    from_: Optional["GetNewestEmailResponseFrom"] = Field(alias="From", default=None)
    has_attachments: Optional[bool] = Field(alias="HasAttachments", default=None)
    id: Optional[str] = Field(alias="ID", default=None)
    importance: Optional[str] = Field(alias="Importance", default=None)
    parent_folders: Optional[
        list["GetNewestEmailResponseParentFoldersArrayItemRef"]
    ] = Field(alias="ParentFolders", default=None)
    subject: Optional[str] = Field(alias="Subject", default=None)
    thread_id: Optional[str] = Field(alias="ThreadID", default=None)
    to: Optional[list["GetNewestEmailResponseToArrayItemRef"]] = Field(
        alias="To", default=None
    )
    type_: Optional[str] = Field(alias="Type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetNewestEmailResponse"], src_dict: Dict[str, Any]):
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
