from enum import Enum


class CreateSignRequestResponseSignersSignerDecisionType(str, Enum):
    DECLINED = "declined"
    SIGNED = "signed"

    def __str__(self) -> str:
        return str(self.value)
