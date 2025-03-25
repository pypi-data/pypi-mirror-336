"""Contains all the data models used in inputs/outputs"""

from .apply_gmail_label_request import ApplyGmailLabelRequest
from .apply_gmail_label_response import ApplyGmailLabelResponse
from .archive_email_response import ArchiveEmailResponse
from .create_calendar_event_request import CreateCalendarEventRequest
from .create_calendar_event_request_show_as import CreateCalendarEventRequestShowAs
from .create_calendar_event_request_visibility import (
    CreateCalendarEventRequestVisibility,
)
from .create_calendar_event_response import CreateCalendarEventResponse
from .create_calendar_event_response_creator import CreateCalendarEventResponseCreator
from .create_calendar_event_response_end import CreateCalendarEventResponseEnd
from .create_calendar_event_response_organizer import (
    CreateCalendarEventResponseOrganizer,
)
from .create_calendar_event_response_reminders import (
    CreateCalendarEventResponseReminders,
)
from .create_calendar_event_response_show_as import CreateCalendarEventResponseShowAs
from .create_calendar_event_response_start import CreateCalendarEventResponseStart
from .create_calendar_event_response_visibility import (
    CreateCalendarEventResponseVisibility,
)
from .default_error import DefaultError
from .delete_email_response import DeleteEmailResponse
from .download_attachment_response import DownloadAttachmentResponse
from .forward_event_request import ForwardEventRequest
from .forward_mail_v2_body import ForwardMailV2Body
from .forward_mail_v2_request import ForwardMailV2Request
from .forward_mail_v2_response import ForwardMailV2Response
from .get_calendar_list import GetCalendarList
from .get_email_by_idv2_response import GetEmailByIDV2Response
from .get_email_by_idv2_response_attachments_array_item_ref import (
    GetEmailByIDV2ResponseAttachmentsArrayItemRef,
)
from .get_email_by_idv2_response_bcc_array_item_ref import (
    GetEmailByIDV2ResponseBCCArrayItemRef,
)
from .get_email_by_idv2_response_categories_array_item_ref import (
    GetEmailByIDV2ResponseCategoriesArrayItemRef,
)
from .get_email_by_idv2_response_categories_id import GetEmailByIDV2ResponseCategoriesID
from .get_email_by_idv2_response_categories_name import (
    GetEmailByIDV2ResponseCategoriesName,
)
from .get_email_by_idv2_response_cc_array_item_ref import (
    GetEmailByIDV2ResponseCCArrayItemRef,
)
from .get_email_by_idv2_response_from import GetEmailByIDV2ResponseFrom
from .get_email_by_idv2_response_importance import GetEmailByIDV2ResponseImportance
from .get_email_by_idv2_response_parent_folders_array_item_ref import (
    GetEmailByIDV2ResponseParentFoldersArrayItemRef,
)
from .get_email_by_idv2_response_to_array_item_ref import (
    GetEmailByIDV2ResponseToArrayItemRef,
)
from .get_email_by_idv2_response_type import GetEmailByIDV2ResponseType
from .get_email_labels import GetEmailLabels
from .get_event_by_id_response import GetEventByIDResponse
from .get_event_by_id_response_attachments_array_item_ref import (
    GetEventByIDResponseAttachmentsArrayItemRef,
)
from .get_event_by_id_response_attendees_array_item_ref import (
    GetEventByIDResponseAttendeesArrayItemRef,
)
from .get_event_by_id_response_attendees_response_status import (
    GetEventByIDResponseAttendeesResponseStatus,
)
from .get_event_by_id_response_conference_data import GetEventByIDResponseConferenceData
from .get_event_by_id_response_conference_data_conference_solution import (
    GetEventByIDResponseConferenceDataConferenceSolution,
)
from .get_event_by_id_response_conference_data_conference_solution_key import (
    GetEventByIDResponseConferenceDataConferenceSolutionKey,
)
from .get_event_by_id_response_conference_data_conference_solution_key_type import (
    GetEventByIDResponseConferenceDataConferenceSolutionKeyType,
)
from .get_event_by_id_response_conference_data_create_request import (
    GetEventByIDResponseConferenceDataCreateRequest,
)
from .get_event_by_id_response_conference_data_create_request_conference_solution_key import (
    GetEventByIDResponseConferenceDataCreateRequestConferenceSolutionKey,
)
from .get_event_by_id_response_conference_data_create_request_conference_solution_key_type import (
    GetEventByIDResponseConferenceDataCreateRequestConferenceSolutionKeyType,
)
from .get_event_by_id_response_conference_data_create_request_status import (
    GetEventByIDResponseConferenceDataCreateRequestStatus,
)
from .get_event_by_id_response_conference_data_create_request_status_status_code import (
    GetEventByIDResponseConferenceDataCreateRequestStatusStatusCode,
)
from .get_event_by_id_response_conference_data_entry_points_array_item_ref import (
    GetEventByIDResponseConferenceDataEntryPointsArrayItemRef,
)
from .get_event_by_id_response_conference_data_entry_points_entry_point_type import (
    GetEventByIDResponseConferenceDataEntryPointsEntryPointType,
)
from .get_event_by_id_response_creator import GetEventByIDResponseCreator
from .get_event_by_id_response_end import GetEventByIDResponseEnd
from .get_event_by_id_response_event_type import GetEventByIDResponseEventType
from .get_event_by_id_response_gadget import GetEventByIDResponseGadget
from .get_event_by_id_response_gadget_display import GetEventByIDResponseGadgetDisplay
from .get_event_by_id_response_organizer import GetEventByIDResponseOrganizer
from .get_event_by_id_response_original_start_time import (
    GetEventByIDResponseOriginalStartTime,
)
from .get_event_by_id_response_reminders import GetEventByIDResponseReminders
from .get_event_by_id_response_reminders_overrides_array_item_ref import (
    GetEventByIDResponseRemindersOverridesArrayItemRef,
)
from .get_event_by_id_response_reminders_overrides_method import (
    GetEventByIDResponseRemindersOverridesMethod,
)
from .get_event_by_id_response_source import GetEventByIDResponseSource
from .get_event_by_id_response_start import GetEventByIDResponseStart
from .get_event_by_id_response_status import GetEventByIDResponseStatus
from .get_event_by_id_response_transparency import GetEventByIDResponseTransparency
from .get_event_by_id_response_visibility import GetEventByIDResponseVisibility
from .get_newest_email_response import GetNewestEmailResponse
from .get_newest_email_response_attachments_array_item_ref import (
    GetNewestEmailResponseAttachmentsArrayItemRef,
)
from .get_newest_email_response_categories_array_item_ref import (
    GetNewestEmailResponseCategoriesArrayItemRef,
)
from .get_newest_email_response_from import GetNewestEmailResponseFrom
from .get_newest_email_response_parent_folders_array_item_ref import (
    GetNewestEmailResponseParentFoldersArrayItemRef,
)
from .get_newest_email_response_to_array_item_ref import (
    GetNewestEmailResponseToArrayItemRef,
)
from .get_single_label_by_id_response import GetSingleLabelByIDResponse
from .list_calendar_event import ListCalendarEvent
from .list_calendar_event_attendees_array_item_ref import (
    ListCalendarEventAttendeesArrayItemRef,
)
from .list_email import ListEmail
from .list_email_bcc_array_item_ref import ListEmailBCCArrayItemRef
from .list_email_categories_array_item_ref import ListEmailCategoriesArrayItemRef
from .list_email_categories_id import ListEmailCategoriesID
from .list_email_categories_name import ListEmailCategoriesName
from .list_email_cc_array_item_ref import ListEmailCCArrayItemRef
from .list_email_from import ListEmailFrom
from .list_email_parent_folders_array_item_ref import ListEmailParentFoldersArrayItemRef
from .list_email_to_array_item_ref import ListEmailToArrayItemRef
from .list_email_type import ListEmailType
from .mark_email_read_unread_response import MarkEmailReadUnreadResponse
from .move_email_response import MoveEmailResponse
from .remove_gmail_label_request import RemoveGmailLabelRequest
from .remove_gmail_label_response import RemoveGmailLabelResponse
from .reply_to_email_v2_body import ReplyToEmailV2Body
from .reply_to_email_v2_request import ReplyToEmailV2Request
from .reply_to_email_v2_request_importance import ReplyToEmailV2RequestImportance
from .reply_to_email_v2_response import ReplyToEmailV2Response
from .respond_to_event_invitation_request import RespondToEventInvitationRequest
from .respond_to_event_invitation_request_response import (
    RespondToEventInvitationRequestResponse,
)
from .send_email_body import SendEmailBody
from .send_email_request import SendEmailRequest
from .send_email_request_importance import SendEmailRequestImportance
from .send_email_response import SendEmailResponse
from .send_email_response_importance import SendEmailResponseImportance
from .turn_off_automatic_replies_response import TurnOffAutomaticRepliesResponse
from .turn_on_automatic_replies_request import TurnOnAutomaticRepliesRequest
from .turn_on_automatic_replies_response import TurnOnAutomaticRepliesResponse
from .update_calendar_event_request import UpdateCalendarEventRequest
from .update_calendar_event_request_change_optional_attendees import (
    UpdateCalendarEventRequestChangeOptionalAttendees,
)
from .update_calendar_event_request_change_required_attendees import (
    UpdateCalendarEventRequestChangeRequiredAttendees,
)
from .update_calendar_event_request_change_resource_attendees import (
    UpdateCalendarEventRequestChangeResourceAttendees,
)
from .update_calendar_event_request_show_as import UpdateCalendarEventRequestShowAs
from .update_calendar_event_request_visibility import (
    UpdateCalendarEventRequestVisibility,
)
from .update_calendar_event_response import UpdateCalendarEventResponse
from .update_calendar_event_response_creator import UpdateCalendarEventResponseCreator
from .update_calendar_event_response_end import UpdateCalendarEventResponseEnd
from .update_calendar_event_response_organizer import (
    UpdateCalendarEventResponseOrganizer,
)
from .update_calendar_event_response_reminders import (
    UpdateCalendarEventResponseReminders,
)
from .update_calendar_event_response_show_as import UpdateCalendarEventResponseShowAs
from .update_calendar_event_response_start import UpdateCalendarEventResponseStart
from .update_calendar_event_response_visibility import (
    UpdateCalendarEventResponseVisibility,
)

__all__ = (
    "ApplyGmailLabelRequest",
    "ApplyGmailLabelResponse",
    "ArchiveEmailResponse",
    "CreateCalendarEventRequest",
    "CreateCalendarEventRequestShowAs",
    "CreateCalendarEventRequestVisibility",
    "CreateCalendarEventResponse",
    "CreateCalendarEventResponseCreator",
    "CreateCalendarEventResponseEnd",
    "CreateCalendarEventResponseOrganizer",
    "CreateCalendarEventResponseReminders",
    "CreateCalendarEventResponseShowAs",
    "CreateCalendarEventResponseStart",
    "CreateCalendarEventResponseVisibility",
    "DefaultError",
    "DeleteEmailResponse",
    "DownloadAttachmentResponse",
    "ForwardEventRequest",
    "ForwardMailV2Body",
    "ForwardMailV2Request",
    "ForwardMailV2Response",
    "GetCalendarList",
    "GetEmailByIDV2Response",
    "GetEmailByIDV2ResponseAttachmentsArrayItemRef",
    "GetEmailByIDV2ResponseBCCArrayItemRef",
    "GetEmailByIDV2ResponseCategoriesArrayItemRef",
    "GetEmailByIDV2ResponseCategoriesID",
    "GetEmailByIDV2ResponseCategoriesName",
    "GetEmailByIDV2ResponseCCArrayItemRef",
    "GetEmailByIDV2ResponseFrom",
    "GetEmailByIDV2ResponseImportance",
    "GetEmailByIDV2ResponseParentFoldersArrayItemRef",
    "GetEmailByIDV2ResponseToArrayItemRef",
    "GetEmailByIDV2ResponseType",
    "GetEmailLabels",
    "GetEventByIDResponse",
    "GetEventByIDResponseAttachmentsArrayItemRef",
    "GetEventByIDResponseAttendeesArrayItemRef",
    "GetEventByIDResponseAttendeesResponseStatus",
    "GetEventByIDResponseConferenceData",
    "GetEventByIDResponseConferenceDataConferenceSolution",
    "GetEventByIDResponseConferenceDataConferenceSolutionKey",
    "GetEventByIDResponseConferenceDataConferenceSolutionKeyType",
    "GetEventByIDResponseConferenceDataCreateRequest",
    "GetEventByIDResponseConferenceDataCreateRequestConferenceSolutionKey",
    "GetEventByIDResponseConferenceDataCreateRequestConferenceSolutionKeyType",
    "GetEventByIDResponseConferenceDataCreateRequestStatus",
    "GetEventByIDResponseConferenceDataCreateRequestStatusStatusCode",
    "GetEventByIDResponseConferenceDataEntryPointsArrayItemRef",
    "GetEventByIDResponseConferenceDataEntryPointsEntryPointType",
    "GetEventByIDResponseCreator",
    "GetEventByIDResponseEnd",
    "GetEventByIDResponseEventType",
    "GetEventByIDResponseGadget",
    "GetEventByIDResponseGadgetDisplay",
    "GetEventByIDResponseOrganizer",
    "GetEventByIDResponseOriginalStartTime",
    "GetEventByIDResponseReminders",
    "GetEventByIDResponseRemindersOverridesArrayItemRef",
    "GetEventByIDResponseRemindersOverridesMethod",
    "GetEventByIDResponseSource",
    "GetEventByIDResponseStart",
    "GetEventByIDResponseStatus",
    "GetEventByIDResponseTransparency",
    "GetEventByIDResponseVisibility",
    "GetNewestEmailResponse",
    "GetNewestEmailResponseAttachmentsArrayItemRef",
    "GetNewestEmailResponseCategoriesArrayItemRef",
    "GetNewestEmailResponseFrom",
    "GetNewestEmailResponseParentFoldersArrayItemRef",
    "GetNewestEmailResponseToArrayItemRef",
    "GetSingleLabelByIDResponse",
    "ListCalendarEvent",
    "ListCalendarEventAttendeesArrayItemRef",
    "ListEmail",
    "ListEmailBCCArrayItemRef",
    "ListEmailCategoriesArrayItemRef",
    "ListEmailCategoriesID",
    "ListEmailCategoriesName",
    "ListEmailCCArrayItemRef",
    "ListEmailFrom",
    "ListEmailParentFoldersArrayItemRef",
    "ListEmailToArrayItemRef",
    "ListEmailType",
    "MarkEmailReadUnreadResponse",
    "MoveEmailResponse",
    "RemoveGmailLabelRequest",
    "RemoveGmailLabelResponse",
    "ReplyToEmailV2Body",
    "ReplyToEmailV2Request",
    "ReplyToEmailV2RequestImportance",
    "ReplyToEmailV2Response",
    "RespondToEventInvitationRequest",
    "RespondToEventInvitationRequestResponse",
    "SendEmailBody",
    "SendEmailRequest",
    "SendEmailRequestImportance",
    "SendEmailResponse",
    "SendEmailResponseImportance",
    "TurnOffAutomaticRepliesResponse",
    "TurnOnAutomaticRepliesRequest",
    "TurnOnAutomaticRepliesResponse",
    "UpdateCalendarEventRequest",
    "UpdateCalendarEventRequestChangeOptionalAttendees",
    "UpdateCalendarEventRequestChangeRequiredAttendees",
    "UpdateCalendarEventRequestChangeResourceAttendees",
    "UpdateCalendarEventRequestShowAs",
    "UpdateCalendarEventRequestVisibility",
    "UpdateCalendarEventResponse",
    "UpdateCalendarEventResponseCreator",
    "UpdateCalendarEventResponseEnd",
    "UpdateCalendarEventResponseOrganizer",
    "UpdateCalendarEventResponseReminders",
    "UpdateCalendarEventResponseShowAs",
    "UpdateCalendarEventResponseStart",
    "UpdateCalendarEventResponseVisibility",
)
