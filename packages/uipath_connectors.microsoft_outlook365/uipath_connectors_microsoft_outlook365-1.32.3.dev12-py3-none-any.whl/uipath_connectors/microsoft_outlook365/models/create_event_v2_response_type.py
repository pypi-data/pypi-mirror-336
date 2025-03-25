from enum import Enum


class CreateEventV2ResponseType(str, Enum):
    EXCEPTION = "exception"
    OCCURRENCE = "occurrence"
    SERIES_MASTER = "seriesMaster"
    SINGLE_INSTANCE = "singleInstance"

    def __str__(self) -> str:
        return str(self.value)
