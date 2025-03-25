from .apply_gmail_label import (
    apply_gmail_label as _apply_gmail_label,
    apply_gmail_label_async as _apply_gmail_label_async,
)
from ..models.apply_gmail_label_request import ApplyGmailLabelRequest
from ..models.apply_gmail_label_response import ApplyGmailLabelResponse
from ..models.default_error import DefaultError
from typing import cast
from .archive_email import (
    archive_email as _archive_email,
    archive_email_async as _archive_email_async,
)
from ..models.archive_email_response import ArchiveEmailResponse
from .create_calendar_event import (
    create_calendar_event as _create_calendar_event,
    create_calendar_event_async as _create_calendar_event_async,
)
from ..models.create_calendar_event_request import CreateCalendarEventRequest
from ..models.create_calendar_event_response import CreateCalendarEventResponse
from .delete_email import (
    delete_email as _delete_email,
    delete_email_async as _delete_email_async,
)
from ..models.delete_email_response import DeleteEmailResponse
from .download_attachment import (
    download_attachment as _download_attachment,
    download_attachment_async as _download_attachment_async,
)
from ..models.download_attachment_response import DownloadAttachmentResponse
from ..types import File
from io import BytesIO
from .download_email import (
    download_email as _download_email,
    download_email_async as _download_email_async,
)
from .forward_event import (
    forward_event as _forward_event,
    forward_event_async as _forward_event_async,
)
from ..models.forward_event_request import ForwardEventRequest
from .forward_mail_v2 import (
    forward_mail_v2 as _forward_mail_v2,
    forward_mail_v2_async as _forward_mail_v2_async,
)
from ..models.forward_mail_v2_body import ForwardMailV2Body
from ..models.forward_mail_v2_request import ForwardMailV2Request
from ..models.forward_mail_v2_response import ForwardMailV2Response
from .curated_calendar_list import (
    get_calendar_list as _get_calendar_list,
    get_calendar_list_async as _get_calendar_list_async,
)
from ..models.get_calendar_list import GetCalendarList
from .normalized_message import (
    get_email_by_idv2 as _get_email_by_idv2,
    get_email_by_idv2_async as _get_email_by_idv2_async,
)
from ..models.get_email_by_idv2_response import GetEmailByIDV2Response
from .folder import (
    get_email_labels as _get_email_labels,
    get_email_labels_async as _get_email_labels_async,
    get_single_label_by_id as _get_single_label_by_id,
    get_single_label_by_id_async as _get_single_label_by_id_async,
)
from ..models.get_email_labels import GetEmailLabels
from ..models.get_single_label_by_id_response import GetSingleLabelByIDResponse
from .calendar import (
    get_event_by_id as _get_event_by_id,
    get_event_by_id_async as _get_event_by_id_async,
)
from ..models.get_event_by_id_response import GetEventByIDResponse
from .get_newest_email import (
    get_newest_email as _get_newest_email,
    get_newest_email_async as _get_newest_email_async,
)
from ..models.get_newest_email_response import GetNewestEmailResponse
from .list_calendar_event import (
    list_calendar_event as _list_calendar_event,
    list_calendar_event_async as _list_calendar_event_async,
)
from ..models.list_calendar_event import ListCalendarEvent
from dateutil.parser import isoparse
import datetime
from .list_email import (
    list_email as _list_email,
    list_email_async as _list_email_async,
)
from ..models.list_email import ListEmail
from .mark_email_read_unread import (
    mark_email_read_unread as _mark_email_read_unread,
    mark_email_read_unread_async as _mark_email_read_unread_async,
)
from ..models.mark_email_read_unread_response import MarkEmailReadUnreadResponse
from .move_email import (
    move_email as _move_email,
    move_email_async as _move_email_async,
)
from ..models.move_email_response import MoveEmailResponse
from .remove_gmail_label import (
    remove_gmail_label as _remove_gmail_label,
    remove_gmail_label_async as _remove_gmail_label_async,
)
from ..models.remove_gmail_label_request import RemoveGmailLabelRequest
from ..models.remove_gmail_label_response import RemoveGmailLabelResponse
from .email_reply import (
    reply_to_email_v2 as _reply_to_email_v2,
    reply_to_email_v2_async as _reply_to_email_v2_async,
)
from ..models.reply_to_email_v2_body import ReplyToEmailV2Body
from ..models.reply_to_email_v2_request import ReplyToEmailV2Request
from ..models.reply_to_email_v2_response import ReplyToEmailV2Response
from .respond_to_event_invitation import (
    respond_to_event_invitation as _respond_to_event_invitation,
    respond_to_event_invitation_async as _respond_to_event_invitation_async,
)
from ..models.respond_to_event_invitation_request import RespondToEventInvitationRequest
from .send_email import (
    send_email as _send_email,
    send_email_async as _send_email_async,
)
from ..models.send_email_body import SendEmailBody
from ..models.send_email_request import SendEmailRequest
from ..models.send_email_response import SendEmailResponse
from .turn_off_automatic_replies import (
    turn_off_automatic_replies as _turn_off_automatic_replies,
    turn_off_automatic_replies_async as _turn_off_automatic_replies_async,
)
from ..models.turn_off_automatic_replies_response import TurnOffAutomaticRepliesResponse
from .turn_on_automatic_replies import (
    turn_on_automatic_replies as _turn_on_automatic_replies,
    turn_on_automatic_replies_async as _turn_on_automatic_replies_async,
)
from ..models.turn_on_automatic_replies_request import TurnOnAutomaticRepliesRequest
from ..models.turn_on_automatic_replies_response import TurnOnAutomaticRepliesResponse
from .update_calendar_event import (
    update_calendar_event as _update_calendar_event,
    update_calendar_event_async as _update_calendar_event_async,
)
from ..models.update_calendar_event_request import UpdateCalendarEventRequest
from ..models.update_calendar_event_response import UpdateCalendarEventResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class GoogleGmail:
    def __init__(self, *, instance_id: str, client: httpx.Client):
        base_url = str(client.base_url).rstrip("/")
        new_headers = {
            k: v for k, v in client.headers.items() if k not in ["content-type"]
        }
        new_client = httpx.Client(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        new_client_async = httpx.AsyncClient(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        self.client = (
            Client(
                base_url="",  # this will be overridden by the base_url in the Client constructor
            )
            .set_httpx_client(new_client)
            .set_async_httpx_client(new_client_async)
        )

    def apply_gmail_label(
        self,
        *,
        body: ApplyGmailLabelRequest,
        id: str,
    ) -> Optional[Union[ApplyGmailLabelResponse, DefaultError]]:
        return _apply_gmail_label(
            client=self.client,
            body=body,
            id=id,
        )

    async def apply_gmail_label_async(
        self,
        *,
        body: ApplyGmailLabelRequest,
        id: str,
    ) -> Optional[Union[ApplyGmailLabelResponse, DefaultError]]:
        return await _apply_gmail_label_async(
            client=self.client,
            body=body,
            id=id,
        )

    def archive_email(
        self,
        *,
        id: str,
    ) -> Optional[Union[ArchiveEmailResponse, DefaultError]]:
        return _archive_email(
            client=self.client,
            id=id,
        )

    async def archive_email_async(
        self,
        *,
        id: str,
    ) -> Optional[Union[ArchiveEmailResponse, DefaultError]]:
        return await _archive_email_async(
            client=self.client,
            id=id,
        )

    def create_calendar_event(
        self,
        *,
        body: CreateCalendarEventRequest,
        add_conference_data: Optional[bool] = False,
        send_notifications: Optional[str] = "all",
        calendar: Optional[str] = None,
        calendar_lookup: Any,
    ) -> Optional[Union[CreateCalendarEventResponse, DefaultError]]:
        return _create_calendar_event(
            client=self.client,
            body=body,
            add_conference_data=add_conference_data,
            send_notifications=send_notifications,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
        )

    async def create_calendar_event_async(
        self,
        *,
        body: CreateCalendarEventRequest,
        add_conference_data: Optional[bool] = False,
        send_notifications: Optional[str] = "all",
        calendar: Optional[str] = None,
        calendar_lookup: Any,
    ) -> Optional[Union[CreateCalendarEventResponse, DefaultError]]:
        return await _create_calendar_event_async(
            client=self.client,
            body=body,
            add_conference_data=add_conference_data,
            send_notifications=send_notifications,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
        )

    def delete_email(
        self,
        *,
        id: str,
        permanently_delete: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, DeleteEmailResponse]]:
        return _delete_email(
            client=self.client,
            id=id,
            permanently_delete=permanently_delete,
        )

    async def delete_email_async(
        self,
        *,
        id: str,
        permanently_delete: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, DeleteEmailResponse]]:
        return await _delete_email_async(
            client=self.client,
            id=id,
            permanently_delete=permanently_delete,
        )

    def download_attachment(
        self,
        id: str,
        *,
        file_name: Optional[str] = None,
        exclude_inline_attachment: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, File]]:
        return _download_attachment(
            client=self.client,
            id=id,
            file_name=file_name,
            exclude_inline_attachment=exclude_inline_attachment,
        )

    async def download_attachment_async(
        self,
        id: str,
        *,
        file_name: Optional[str] = None,
        exclude_inline_attachment: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, File]]:
        return await _download_attachment_async(
            client=self.client,
            id=id,
            file_name=file_name,
            exclude_inline_attachment=exclude_inline_attachment,
        )

    def download_email(
        self,
        *,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return _download_email(
            client=self.client,
            id=id,
        )

    async def download_email_async(
        self,
        *,
        id: str,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _download_email_async(
            client=self.client,
            id=id,
        )

    def forward_event(
        self,
        id: str,
        *,
        body: ForwardEventRequest,
        calendar_id: Optional[str] = None,
        calendar_id_lookup: Any,
        forward_series: Optional[bool] = False,
    ) -> Optional[Union[Any, DefaultError]]:
        return _forward_event(
            client=self.client,
            id=id,
            body=body,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
            forward_series=forward_series,
        )

    async def forward_event_async(
        self,
        id: str,
        *,
        body: ForwardEventRequest,
        calendar_id: Optional[str] = None,
        calendar_id_lookup: Any,
        forward_series: Optional[bool] = False,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _forward_event_async(
            client=self.client,
            id=id,
            body=body,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
            forward_series=forward_series,
        )

    def forward_mail_v2(
        self,
        *,
        body: ForwardMailV2Body,
        id: str,
        save_as_draft: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, ForwardMailV2Response]]:
        return _forward_mail_v2(
            client=self.client,
            body=body,
            id=id,
            save_as_draft=save_as_draft,
        )

    async def forward_mail_v2_async(
        self,
        *,
        body: ForwardMailV2Body,
        id: str,
        save_as_draft: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, ForwardMailV2Response]]:
        return await _forward_mail_v2_async(
            client=self.client,
            body=body,
            id=id,
            save_as_draft=save_as_draft,
        )

    def get_calendar_list(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        parent_reference: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetCalendarList"]]]:
        return _get_calendar_list(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            parent_reference=parent_reference,
        )

    async def get_calendar_list_async(
        self,
        *,
        next_page: Optional[str] = None,
        page_size: Optional[int] = None,
        parent_reference: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetCalendarList"]]]:
        return await _get_calendar_list_async(
            client=self.client,
            next_page=next_page,
            page_size=page_size,
            parent_reference=parent_reference,
        )

    def get_email_by_idv2(
        self,
        normalized_message_id: str,
    ) -> Optional[Union[DefaultError, GetEmailByIDV2Response]]:
        return _get_email_by_idv2(
            client=self.client,
            normalized_message_id=normalized_message_id,
        )

    async def get_email_by_idv2_async(
        self,
        normalized_message_id: str,
    ) -> Optional[Union[DefaultError, GetEmailByIDV2Response]]:
        return await _get_email_by_idv2_async(
            client=self.client,
            normalized_message_id=normalized_message_id,
        )

    def get_email_labels(
        self,
        *,
        parent_reference: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetEmailLabels"]]]:
        return _get_email_labels(
            client=self.client,
            parent_reference=parent_reference,
        )

    async def get_email_labels_async(
        self,
        *,
        parent_reference: Optional[str] = None,
    ) -> Optional[Union[DefaultError, list["GetEmailLabels"]]]:
        return await _get_email_labels_async(
            client=self.client,
            parent_reference=parent_reference,
        )

    def get_single_label_by_id(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetSingleLabelByIDResponse]]:
        return _get_single_label_by_id(
            client=self.client,
            id=id,
        )

    async def get_single_label_by_id_async(
        self,
        id: str,
    ) -> Optional[Union[DefaultError, GetSingleLabelByIDResponse]]:
        return await _get_single_label_by_id_async(
            client=self.client,
            id=id,
        )

    def get_event_by_id(
        self,
        id: str,
        *,
        max_attendees: Optional[str] = None,
        time_zone: Optional[str] = None,
        calendar_id: Optional[str] = None,
        calendar_id_lookup: Any,
    ) -> Optional[Union[DefaultError, GetEventByIDResponse]]:
        return _get_event_by_id(
            client=self.client,
            id=id,
            max_attendees=max_attendees,
            time_zone=time_zone,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
        )

    async def get_event_by_id_async(
        self,
        id: str,
        *,
        max_attendees: Optional[str] = None,
        time_zone: Optional[str] = None,
        calendar_id: Optional[str] = None,
        calendar_id_lookup: Any,
    ) -> Optional[Union[DefaultError, GetEventByIDResponse]]:
        return await _get_event_by_id_async(
            client=self.client,
            id=id,
            max_attendees=max_attendees,
            time_zone=time_zone,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
        )

    def get_newest_email(
        self,
        *,
        unread_only: Optional[bool] = False,
        important_only: Optional[bool] = False,
        email_folder: str,
        email_folder_lookup: Any,
        additional_filter: Optional[str] = None,
        with_attachment_only: Optional[bool] = False,
        mark_as_read: Optional[bool] = False,
        starred_only: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, GetNewestEmailResponse]]:
        return _get_newest_email(
            client=self.client,
            unread_only=unread_only,
            important_only=important_only,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            additional_filter=additional_filter,
            with_attachment_only=with_attachment_only,
            mark_as_read=mark_as_read,
            starred_only=starred_only,
        )

    async def get_newest_email_async(
        self,
        *,
        unread_only: Optional[bool] = False,
        important_only: Optional[bool] = False,
        email_folder: str,
        email_folder_lookup: Any,
        additional_filter: Optional[str] = None,
        with_attachment_only: Optional[bool] = False,
        mark_as_read: Optional[bool] = False,
        starred_only: Optional[bool] = False,
    ) -> Optional[Union[DefaultError, GetNewestEmailResponse]]:
        return await _get_newest_email_async(
            client=self.client,
            unread_only=unread_only,
            important_only=important_only,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            additional_filter=additional_filter,
            with_attachment_only=with_attachment_only,
            mark_as_read=mark_as_read,
            starred_only=starred_only,
        )

    def list_calendar_event(
        self,
        *,
        timezone: Optional[str] = "UTC",
        timezone_lookup: Any,
        from_: datetime.datetime,
        simple_search: Optional[str] = None,
        until: datetime.datetime,
        calendar: Optional[str] = None,
        calendar_lookup: Any,
        limit: Optional[str] = "50",
    ) -> Optional[Union[DefaultError, list["ListCalendarEvent"]]]:
        return _list_calendar_event(
            client=self.client,
            timezone=timezone,
            timezone_lookup=timezone_lookup,
            from_=from_,
            simple_search=simple_search,
            until=until,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            limit=limit,
        )

    async def list_calendar_event_async(
        self,
        *,
        timezone: Optional[str] = "UTC",
        timezone_lookup: Any,
        from_: datetime.datetime,
        simple_search: Optional[str] = None,
        until: datetime.datetime,
        calendar: Optional[str] = None,
        calendar_lookup: Any,
        limit: Optional[str] = "50",
    ) -> Optional[Union[DefaultError, list["ListCalendarEvent"]]]:
        return await _list_calendar_event_async(
            client=self.client,
            timezone=timezone,
            timezone_lookup=timezone_lookup,
            from_=from_,
            simple_search=simple_search,
            until=until,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            limit=limit,
        )

    def list_email(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        with_attachments_only: Optional[bool] = False,
        important_only: Optional[bool] = False,
        mark_as_read: Optional[bool] = False,
        include_subfolders: Optional[bool] = False,
        starred_only: Optional[bool] = False,
        limit_emails_to_first: Optional[str] = "50",
        email_folder: str,
        email_folder_lookup: Any,
        unread_only: Optional[bool] = False,
        additional_filters: str,
    ) -> Optional[Union[DefaultError, list["ListEmail"]]]:
        return _list_email(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            with_attachments_only=with_attachments_only,
            important_only=important_only,
            mark_as_read=mark_as_read,
            include_subfolders=include_subfolders,
            starred_only=starred_only,
            limit_emails_to_first=limit_emails_to_first,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            unread_only=unread_only,
            additional_filters=additional_filters,
        )

    async def list_email_async(
        self,
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        with_attachments_only: Optional[bool] = False,
        important_only: Optional[bool] = False,
        mark_as_read: Optional[bool] = False,
        include_subfolders: Optional[bool] = False,
        starred_only: Optional[bool] = False,
        limit_emails_to_first: Optional[str] = "50",
        email_folder: str,
        email_folder_lookup: Any,
        unread_only: Optional[bool] = False,
        additional_filters: str,
    ) -> Optional[Union[DefaultError, list["ListEmail"]]]:
        return await _list_email_async(
            client=self.client,
            page_size=page_size,
            next_page=next_page,
            with_attachments_only=with_attachments_only,
            important_only=important_only,
            mark_as_read=mark_as_read,
            include_subfolders=include_subfolders,
            starred_only=starred_only,
            limit_emails_to_first=limit_emails_to_first,
            email_folder=email_folder,
            email_folder_lookup=email_folder_lookup,
            unread_only=unread_only,
            additional_filters=additional_filters,
        )

    def mark_email_read_unread(
        self,
        *,
        id: str,
        mark_as: Optional[str] = "read",
    ) -> Optional[Union[DefaultError, MarkEmailReadUnreadResponse]]:
        return _mark_email_read_unread(
            client=self.client,
            id=id,
            mark_as=mark_as,
        )

    async def mark_email_read_unread_async(
        self,
        *,
        id: str,
        mark_as: Optional[str] = "read",
    ) -> Optional[Union[DefaultError, MarkEmailReadUnreadResponse]]:
        return await _mark_email_read_unread_async(
            client=self.client,
            id=id,
            mark_as=mark_as,
        )

    def move_email(
        self,
        *,
        add_label_id: str,
        add_label_id_lookup: Any,
        id: str,
    ) -> Optional[Union[DefaultError, MoveEmailResponse]]:
        return _move_email(
            client=self.client,
            add_label_id=add_label_id,
            add_label_id_lookup=add_label_id_lookup,
            id=id,
        )

    async def move_email_async(
        self,
        *,
        add_label_id: str,
        add_label_id_lookup: Any,
        id: str,
    ) -> Optional[Union[DefaultError, MoveEmailResponse]]:
        return await _move_email_async(
            client=self.client,
            add_label_id=add_label_id,
            add_label_id_lookup=add_label_id_lookup,
            id=id,
        )

    def remove_gmail_label(
        self,
        *,
        body: RemoveGmailLabelRequest,
        id: str,
    ) -> Optional[Union[DefaultError, RemoveGmailLabelResponse]]:
        return _remove_gmail_label(
            client=self.client,
            body=body,
            id=id,
        )

    async def remove_gmail_label_async(
        self,
        *,
        body: RemoveGmailLabelRequest,
        id: str,
    ) -> Optional[Union[DefaultError, RemoveGmailLabelResponse]]:
        return await _remove_gmail_label_async(
            client=self.client,
            body=body,
            id=id,
        )

    def reply_to_email_v2(
        self,
        *,
        body: ReplyToEmailV2Body,
        reply_to_all: Optional[bool] = False,
        id: str,
        save_as_draft: Optional[bool] = None,
    ) -> Optional[Union[DefaultError, ReplyToEmailV2Response]]:
        return _reply_to_email_v2(
            client=self.client,
            body=body,
            reply_to_all=reply_to_all,
            id=id,
            save_as_draft=save_as_draft,
        )

    async def reply_to_email_v2_async(
        self,
        *,
        body: ReplyToEmailV2Body,
        reply_to_all: Optional[bool] = False,
        id: str,
        save_as_draft: Optional[bool] = None,
    ) -> Optional[Union[DefaultError, ReplyToEmailV2Response]]:
        return await _reply_to_email_v2_async(
            client=self.client,
            body=body,
            reply_to_all=reply_to_all,
            id=id,
            save_as_draft=save_as_draft,
        )

    def respond_to_event_invitation(
        self,
        id: str,
        *,
        body: RespondToEventInvitationRequest,
        calendar_id: Optional[str] = None,
        calendar_id_lookup: Any,
        send_notification: Optional[bool] = False,
        apply_on_series: Optional[bool] = False,
    ) -> Optional[Union[Any, DefaultError]]:
        return _respond_to_event_invitation(
            client=self.client,
            id=id,
            body=body,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
            send_notification=send_notification,
            apply_on_series=apply_on_series,
        )

    async def respond_to_event_invitation_async(
        self,
        id: str,
        *,
        body: RespondToEventInvitationRequest,
        calendar_id: Optional[str] = None,
        calendar_id_lookup: Any,
        send_notification: Optional[bool] = False,
        apply_on_series: Optional[bool] = False,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _respond_to_event_invitation_async(
            client=self.client,
            id=id,
            body=body,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
            send_notification=send_notification,
            apply_on_series=apply_on_series,
        )

    def send_email(
        self,
        *,
        body: SendEmailBody,
        save_as_draft: Optional[bool] = True,
    ) -> Optional[Union[DefaultError, SendEmailResponse]]:
        return _send_email(
            client=self.client,
            body=body,
            save_as_draft=save_as_draft,
        )

    async def send_email_async(
        self,
        *,
        body: SendEmailBody,
        save_as_draft: Optional[bool] = True,
    ) -> Optional[Union[DefaultError, SendEmailResponse]]:
        return await _send_email_async(
            client=self.client,
            body=body,
            save_as_draft=save_as_draft,
        )

    def turn_off_automatic_replies(
        self,
    ) -> Optional[Union[DefaultError, TurnOffAutomaticRepliesResponse]]:
        return _turn_off_automatic_replies(
            client=self.client,
        )

    async def turn_off_automatic_replies_async(
        self,
    ) -> Optional[Union[DefaultError, TurnOffAutomaticRepliesResponse]]:
        return await _turn_off_automatic_replies_async(
            client=self.client,
        )

    def turn_on_automatic_replies(
        self,
        *,
        body: TurnOnAutomaticRepliesRequest,
    ) -> Optional[Union[DefaultError, TurnOnAutomaticRepliesResponse]]:
        return _turn_on_automatic_replies(
            client=self.client,
            body=body,
        )

    async def turn_on_automatic_replies_async(
        self,
        *,
        body: TurnOnAutomaticRepliesRequest,
    ) -> Optional[Union[DefaultError, TurnOnAutomaticRepliesResponse]]:
        return await _turn_on_automatic_replies_async(
            client=self.client,
            body=body,
        )

    def update_calendar_event(
        self,
        id: str,
        *,
        body: UpdateCalendarEventRequest,
        calendar: Optional[str] = None,
        calendar_lookup: Any,
        output_timezone: Optional[str] = None,
        output_timezone_lookup: Any,
        add_conference_data: Optional[bool] = None,
        send_notifications: Optional[str] = "All",
    ) -> Optional[Union[DefaultError, UpdateCalendarEventResponse]]:
        return _update_calendar_event(
            client=self.client,
            id=id,
            body=body,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            output_timezone=output_timezone,
            output_timezone_lookup=output_timezone_lookup,
            add_conference_data=add_conference_data,
            send_notifications=send_notifications,
        )

    async def update_calendar_event_async(
        self,
        id: str,
        *,
        body: UpdateCalendarEventRequest,
        calendar: Optional[str] = None,
        calendar_lookup: Any,
        output_timezone: Optional[str] = None,
        output_timezone_lookup: Any,
        add_conference_data: Optional[bool] = None,
        send_notifications: Optional[str] = "All",
    ) -> Optional[Union[DefaultError, UpdateCalendarEventResponse]]:
        return await _update_calendar_event_async(
            client=self.client,
            id=id,
            body=body,
            calendar=calendar,
            calendar_lookup=calendar_lookup,
            output_timezone=output_timezone,
            output_timezone_lookup=output_timezone_lookup,
            add_conference_data=add_conference_data,
            send_notifications=send_notifications,
        )
