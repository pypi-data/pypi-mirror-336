from enum import Enum


class ListSignRequestStatus(str, Enum):
    CANCELLED = "cancelled"
    CONVERTING = "converting"
    CREATED = "created"
    DECLINED = "declined"
    ERROR_CONVERTING = "error_converting"
    ERROR_SENDING = "error_sending"
    EXPIRED = "expired"
    SENT = "sent"
    SIGNED = "signed"
    VIEWED = "viewed"

    def __str__(self) -> str:
        return str(self.value)
