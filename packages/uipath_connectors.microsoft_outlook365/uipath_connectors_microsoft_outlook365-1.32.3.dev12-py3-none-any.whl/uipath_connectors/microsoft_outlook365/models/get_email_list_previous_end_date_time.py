from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type



class GetEmailListPreviousEndDateTime(BaseModel):
    """
    Attributes:
        date_time (Optional[str]): Indicates the end date and time of the previous occurrence. Example:
                2025-03-11T13:00:00.0000000.
        time_zone (Optional[str]): Specifies the time zone for the previous end date and time. Example: UTC.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    date_time: Optional[str] = Field(alias="dateTime", default=None)
    time_zone: Optional[str] = Field(alias="timeZone", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetEmailListPreviousEndDateTime"], src_dict: Dict[str, Any]
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
