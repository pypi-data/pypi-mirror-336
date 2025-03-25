from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_email_by_id_response_bcc_recipients_array_item_ref import (
    GetEmailByIDResponseBccRecipientsArrayItemRef,
)
from ..models.get_email_by_id_response_body import GetEmailByIDResponseBody
from ..models.get_email_by_id_response_cc_recipients_array_item_ref import (
    GetEmailByIDResponseCcRecipientsArrayItemRef,
)
from ..models.get_email_by_id_response_end_date_time import (
    GetEmailByIDResponseEndDateTime,
)
from ..models.get_email_by_id_response_flag import GetEmailByIDResponseFlag
from ..models.get_email_by_id_response_from import GetEmailByIDResponseFrom
from ..models.get_email_by_id_response_importance import GetEmailByIDResponseImportance
from ..models.get_email_by_id_response_inference_classification import (
    GetEmailByIDResponseInferenceClassification,
)
from ..models.get_email_by_id_response_location import GetEmailByIDResponseLocation
from ..models.get_email_by_id_response_previous_end_date_time import (
    GetEmailByIDResponsePreviousEndDateTime,
)
from ..models.get_email_by_id_response_previous_location import (
    GetEmailByIDResponsePreviousLocation,
)
from ..models.get_email_by_id_response_previous_start_date_time import (
    GetEmailByIDResponsePreviousStartDateTime,
)
from ..models.get_email_by_id_response_recurrence import GetEmailByIDResponseRecurrence
from ..models.get_email_by_id_response_reply_to_array_item_ref import (
    GetEmailByIDResponseReplyToArrayItemRef,
)
from ..models.get_email_by_id_response_sender import GetEmailByIDResponseSender
from ..models.get_email_by_id_response_start_date_time import (
    GetEmailByIDResponseStartDateTime,
)
from ..models.get_email_by_id_response_to_recipients_array_item_ref import (
    GetEmailByIDResponseToRecipientsArrayItemRef,
)
import datetime


class GetEmailByIDResponse(BaseModel):
    """
    Attributes:
        bcc_recipients (Optional[list['GetEmailByIDResponseBccRecipientsArrayItemRef']]):
        body (Optional[GetEmailByIDResponseBody]):
        body_preview (Optional[str]):
        categories (Optional[list[str]]):
        cc_recipients (Optional[list['GetEmailByIDResponseCcRecipientsArrayItemRef']]):
        change_key (Optional[str]):
        conversation_id (Optional[str]):
        conversation_index (Optional[str]):
        created_date_time (Optional[datetime.datetime]):
        end_date_time (Optional[GetEmailByIDResponseEndDateTime]):
        flag (Optional[GetEmailByIDResponseFlag]):
        from_ (Optional[GetEmailByIDResponseFrom]):
        has_attachments (Optional[bool]):
        id (Optional[str]):
        importance (Optional[GetEmailByIDResponseImportance]):
        inference_classification (Optional[GetEmailByIDResponseInferenceClassification]):
        internet_message_id (Optional[str]):
        is_all_day (Optional[bool]):
        is_delegated (Optional[bool]):
        is_delivery_receipt_requested (Optional[bool]):
        is_draft (Optional[bool]):
        is_out_of_date (Optional[bool]):
        is_read (Optional[bool]):
        is_read_receipt_requested (Optional[bool]):
        last_modified_date_time (Optional[datetime.datetime]):
        location (Optional[GetEmailByIDResponseLocation]):
        meeting_message_type (Optional[str]):
        meeting_request_type (Optional[str]):
        parent_folder_id (Optional[str]):
        parent_folder_name (Optional[str]):
        previous_end_date_time (Optional[GetEmailByIDResponsePreviousEndDateTime]):
        previous_location (Optional[GetEmailByIDResponsePreviousLocation]):
        previous_start_date_time (Optional[GetEmailByIDResponsePreviousStartDateTime]):
        received_date_time (Optional[datetime.datetime]):
        recurrence (Optional[GetEmailByIDResponseRecurrence]):
        reply_to (Optional[list['GetEmailByIDResponseReplyToArrayItemRef']]):
        response_requested (Optional[bool]):
        sender (Optional[GetEmailByIDResponseSender]):
        sent_date_time (Optional[datetime.datetime]):
        start_date_time (Optional[GetEmailByIDResponseStartDateTime]):
        subject (Optional[str]):
        to_recipients (Optional[list['GetEmailByIDResponseToRecipientsArrayItemRef']]):
        type_ (Optional[str]):
        web_link (Optional[str]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    bcc_recipients: Optional[list["GetEmailByIDResponseBccRecipientsArrayItemRef"]] = (
        Field(alias="bccRecipients", default=None)
    )
    body: Optional["GetEmailByIDResponseBody"] = Field(alias="body", default=None)
    body_preview: Optional[str] = Field(alias="bodyPreview", default=None)
    categories: Optional[list[str]] = Field(alias="categories", default=None)
    cc_recipients: Optional[list["GetEmailByIDResponseCcRecipientsArrayItemRef"]] = (
        Field(alias="ccRecipients", default=None)
    )
    change_key: Optional[str] = Field(alias="changeKey", default=None)
    conversation_id: Optional[str] = Field(alias="conversationId", default=None)
    conversation_index: Optional[str] = Field(alias="conversationIndex", default=None)
    created_date_time: Optional[datetime.datetime] = Field(
        alias="createdDateTime", default=None
    )
    end_date_time: Optional["GetEmailByIDResponseEndDateTime"] = Field(
        alias="endDateTime", default=None
    )
    flag: Optional["GetEmailByIDResponseFlag"] = Field(alias="flag", default=None)
    from_: Optional["GetEmailByIDResponseFrom"] = Field(alias="from", default=None)
    has_attachments: Optional[bool] = Field(alias="hasAttachments", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    importance: Optional["GetEmailByIDResponseImportance"] = Field(
        alias="importance", default=None
    )
    inference_classification: Optional[
        "GetEmailByIDResponseInferenceClassification"
    ] = Field(alias="inferenceClassification", default=None)
    internet_message_id: Optional[str] = Field(alias="internetMessageId", default=None)
    is_all_day: Optional[bool] = Field(alias="isAllDay", default=None)
    is_delegated: Optional[bool] = Field(alias="isDelegated", default=None)
    is_delivery_receipt_requested: Optional[bool] = Field(
        alias="isDeliveryReceiptRequested", default=None
    )
    is_draft: Optional[bool] = Field(alias="isDraft", default=None)
    is_out_of_date: Optional[bool] = Field(alias="isOutOfDate", default=None)
    is_read: Optional[bool] = Field(alias="isRead", default=None)
    is_read_receipt_requested: Optional[bool] = Field(
        alias="isReadReceiptRequested", default=None
    )
    last_modified_date_time: Optional[datetime.datetime] = Field(
        alias="lastModifiedDateTime", default=None
    )
    location: Optional["GetEmailByIDResponseLocation"] = Field(
        alias="location", default=None
    )
    meeting_message_type: Optional[str] = Field(
        alias="meetingMessageType", default=None
    )
    meeting_request_type: Optional[str] = Field(
        alias="meetingRequestType", default=None
    )
    parent_folder_id: Optional[str] = Field(alias="parentFolderId", default=None)
    parent_folder_name: Optional[str] = Field(alias="parentFolderName", default=None)
    previous_end_date_time: Optional["GetEmailByIDResponsePreviousEndDateTime"] = Field(
        alias="previousEndDateTime", default=None
    )
    previous_location: Optional["GetEmailByIDResponsePreviousLocation"] = Field(
        alias="previousLocation", default=None
    )
    previous_start_date_time: Optional["GetEmailByIDResponsePreviousStartDateTime"] = (
        Field(alias="previousStartDateTime", default=None)
    )
    received_date_time: Optional[datetime.datetime] = Field(
        alias="receivedDateTime", default=None
    )
    recurrence: Optional["GetEmailByIDResponseRecurrence"] = Field(
        alias="recurrence", default=None
    )
    reply_to: Optional[list["GetEmailByIDResponseReplyToArrayItemRef"]] = Field(
        alias="replyTo", default=None
    )
    response_requested: Optional[bool] = Field(alias="responseRequested", default=None)
    sender: Optional["GetEmailByIDResponseSender"] = Field(alias="sender", default=None)
    sent_date_time: Optional[datetime.datetime] = Field(
        alias="sentDateTime", default=None
    )
    start_date_time: Optional["GetEmailByIDResponseStartDateTime"] = Field(
        alias="startDateTime", default=None
    )
    subject: Optional[str] = Field(alias="subject", default=None)
    to_recipients: Optional[list["GetEmailByIDResponseToRecipientsArrayItemRef"]] = (
        Field(alias="toRecipients", default=None)
    )
    type_: Optional[str] = Field(alias="type", default=None)
    web_link: Optional[str] = Field(alias="webLink", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetEmailByIDResponse"], src_dict: Dict[str, Any]):
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
