from enum import Enum


class UploadFileVersionResponseSharedLinkEffectivePermission(str, Enum):
    CAN_DOWNLOAD = "can_download"
    CAN_PREVIEW = "can_preview"

    def __str__(self) -> str:
        return str(self.value)
