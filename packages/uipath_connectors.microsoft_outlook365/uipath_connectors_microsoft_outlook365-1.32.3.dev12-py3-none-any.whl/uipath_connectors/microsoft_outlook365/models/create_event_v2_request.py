from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.create_event_v2_request_body import CreateEventV2RequestBody
from ..models.create_event_v2_request_end import CreateEventV2RequestEnd
from ..models.create_event_v2_request_importance import CreateEventV2RequestImportance
from ..models.create_event_v2_request_location import CreateEventV2RequestLocation
from ..models.create_event_v2_request_sensitivity import CreateEventV2RequestSensitivity
from ..models.create_event_v2_request_show_as import CreateEventV2RequestShowAs
from ..models.create_event_v2_request_start import CreateEventV2RequestStart


class CreateEventV2Request(BaseModel):
    """
    Attributes:
        start (Optional[CreateEventV2RequestStart]):
        subject (str): Title → e.g. Event title
        timezone (str): Chose or type a value
        allow_new_time_proposals (Optional[bool]): Indicates if attendees can propose new times for the event. Default:
                True. Example: True.
        body (Optional[CreateEventV2RequestBody]):
        categories (Optional[list[str]]):
        end (Optional[CreateEventV2RequestEnd]):
        hide_attendees (Optional[bool]): Indicates if attendees are hidden from the calendar event. Default: True.
                Example: True.
        importance (Optional[CreateEventV2RequestImportance]): Defines the priority level of the calendar event.
        is_all_day (Optional[bool]): Indicates if the event lasts the entire day. Default: False.
        is_online_meeting (Optional[bool]): Indicates if the meeting is set as an online meeting. Should only be marked
                as true for Teams meeting. Default: True. Example: True.
        location (Optional[CreateEventV2RequestLocation]):
        optional_attendees (Optional[str]): Comma separated list of optional attendees.
        required_attendees (Optional[str]): Comma separated list of required attendees.
        resource_attendees (Optional[str]): Comma separated list of resources, like rooms or equipment, invited to the
                event.
        sensitivity (Optional[CreateEventV2RequestSensitivity]): Indicates the privacy level of the calendar event.
        show_as (Optional[CreateEventV2RequestShowAs]): Indicates how the event appears on the calendar, like busy or
                free.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    subject: str = Field(alias="subject")
    timezone: str = Field(alias="timezone")
    start: Optional["CreateEventV2RequestStart"] = Field(alias="start", default=None)
    allow_new_time_proposals: Optional[bool] = Field(
        alias="allowNewTimeProposals", default=True
    )
    body: Optional["CreateEventV2RequestBody"] = Field(alias="body", default=None)
    categories: Optional[list[str]] = Field(alias="categories", default=None)
    end: Optional["CreateEventV2RequestEnd"] = Field(alias="end", default=None)
    hide_attendees: Optional[bool] = Field(alias="hideAttendees", default=True)
    importance: Optional["CreateEventV2RequestImportance"] = Field(
        alias="importance", default=None
    )
    is_all_day: Optional[bool] = Field(alias="isAllDay", default=False)
    is_online_meeting: Optional[bool] = Field(alias="isOnlineMeeting", default=True)
    location: Optional["CreateEventV2RequestLocation"] = Field(
        alias="location", default=None
    )
    optional_attendees: Optional[str] = Field(alias="optionalAttendees", default=None)
    required_attendees: Optional[str] = Field(alias="requiredAttendees", default=None)
    resource_attendees: Optional[str] = Field(alias="resourceAttendees", default=None)
    sensitivity: Optional["CreateEventV2RequestSensitivity"] = Field(
        alias="sensitivity", default=None
    )
    show_as: Optional["CreateEventV2RequestShowAs"] = Field(
        alias="showAs", default=None
    )

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["CreateEventV2Request"], src_dict: Dict[str, Any]):
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
