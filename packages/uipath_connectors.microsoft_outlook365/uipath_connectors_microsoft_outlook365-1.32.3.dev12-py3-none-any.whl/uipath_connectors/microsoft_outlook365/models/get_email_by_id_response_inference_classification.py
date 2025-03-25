from enum import Enum


class GetEmailByIDResponseInferenceClassification(str, Enum):
    FOCUSED = "focused"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
