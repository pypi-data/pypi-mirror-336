from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_email_by_idv2_response_attachments_array_item_ref import (
    GetEmailByIDV2ResponseAttachmentsArrayItemRef,
)
from ..models.get_email_by_idv2_response_bcc_array_item_ref import (
    GetEmailByIDV2ResponseBCCArrayItemRef,
)
from ..models.get_email_by_idv2_response_categories_array_item_ref import (
    GetEmailByIDV2ResponseCategoriesArrayItemRef,
)
from ..models.get_email_by_idv2_response_cc_array_item_ref import (
    GetEmailByIDV2ResponseCCArrayItemRef,
)
from ..models.get_email_by_idv2_response_from import GetEmailByIDV2ResponseFrom
from ..models.get_email_by_idv2_response_importance import (
    GetEmailByIDV2ResponseImportance,
)
from ..models.get_email_by_idv2_response_parent_folders_array_item_ref import (
    GetEmailByIDV2ResponseParentFoldersArrayItemRef,
)
from ..models.get_email_by_idv2_response_to_array_item_ref import (
    GetEmailByIDV2ResponseToArrayItemRef,
)
from ..models.get_email_by_idv2_response_type import GetEmailByIDV2ResponseType


class GetEmailByIDV2Response(BaseModel):
    """
    Attributes:
        attachments (Optional[list['GetEmailByIDV2ResponseAttachmentsArrayItemRef']]):
        bcc (Optional[list['GetEmailByIDV2ResponseBCCArrayItemRef']]):
        body (Optional[str]):  Example: This is mail body.
                .
        cc (Optional[list['GetEmailByIDV2ResponseCCArrayItemRef']]):
        categories (Optional[list['GetEmailByIDV2ResponseCategoriesArrayItemRef']]):
        from_ (Optional[GetEmailByIDV2ResponseFrom]):
        has_attachments (Optional[bool]):  Example: true.
        id (Optional[str]):
        importance (Optional[GetEmailByIDV2ResponseImportance]):  Example: Normal.
        parent_folders (Optional[list['GetEmailByIDV2ResponseParentFoldersArrayItemRef']]):
        sensitivity (Optional[str]):
        subject (Optional[str]):  Example: Test email with attachment.
        thread_id (Optional[str]):  Example: thread123.
        to (Optional[list['GetEmailByIDV2ResponseToArrayItemRef']]):
        type_ (Optional[GetEmailByIDV2ResponseType]):  Example: email.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attachments: Optional[list["GetEmailByIDV2ResponseAttachmentsArrayItemRef"]] = (
        Field(alias="Attachments", default=None)
    )
    bcc: Optional[list["GetEmailByIDV2ResponseBCCArrayItemRef"]] = Field(
        alias="BCC", default=None
    )
    body: Optional[str] = Field(alias="Body", default=None)
    cc: Optional[list["GetEmailByIDV2ResponseCCArrayItemRef"]] = Field(
        alias="CC", default=None
    )
    categories: Optional[list["GetEmailByIDV2ResponseCategoriesArrayItemRef"]] = Field(
        alias="Categories", default=None
    )
    from_: Optional["GetEmailByIDV2ResponseFrom"] = Field(alias="From", default=None)
    has_attachments: Optional[bool] = Field(alias="HasAttachments", default=None)
    id: Optional[str] = Field(alias="ID", default=None)
    importance: Optional["GetEmailByIDV2ResponseImportance"] = Field(
        alias="Importance", default=None
    )
    parent_folders: Optional[
        list["GetEmailByIDV2ResponseParentFoldersArrayItemRef"]
    ] = Field(alias="ParentFolders", default=None)
    sensitivity: Optional[str] = Field(alias="Sensitivity", default=None)
    subject: Optional[str] = Field(alias="Subject", default=None)
    thread_id: Optional[str] = Field(alias="ThreadID", default=None)
    to: Optional[list["GetEmailByIDV2ResponseToArrayItemRef"]] = Field(
        alias="To", default=None
    )
    type_: Optional["GetEmailByIDV2ResponseType"] = Field(alias="Type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEmailByIDV2Response"], src_dict: Dict[str, Any]):
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
