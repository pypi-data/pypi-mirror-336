from enum import Enum


class CancelSignRequestResponseSignersRole(str, Enum):
    APPROVER = "approver"
    FINAL_COPY_READER = "final_copy_reader"
    SIGNER = "signer"

    def __str__(self) -> str:
        return str(self.value)
