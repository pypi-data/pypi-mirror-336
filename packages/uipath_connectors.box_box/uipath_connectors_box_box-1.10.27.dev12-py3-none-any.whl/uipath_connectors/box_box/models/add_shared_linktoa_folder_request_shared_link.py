from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.add_shared_linktoa_folder_request_shared_link_access import (
    AddSharedLinktoaFolderRequestSharedLinkAccess,
)
from ..models.add_shared_linktoa_folder_request_shared_link_permissions import (
    AddSharedLinktoaFolderRequestSharedLinkPermissions,
)
import datetime


class AddSharedLinktoaFolderRequestSharedLink(BaseModel):
    """
    Attributes:
        access (Optional[AddSharedLinktoaFolderRequestSharedLinkAccess]): The access level for this shared link.

                * `open` - provides access to this item to anyone with this link
                * `company` - only provides access to this item to people the same company
                * `collaborators` - only provides access to this item to people who are
                   collaborators on this item

                If this field is omitted when creating the shared link, the access level
                will be set to the default access level specified by the enterprise admin.
        password (Optional[str]): The password required to access the shared link. Set the
                password to `null` to remove it.

                A password can only be set when `access` is set to `open`.
        permissions (Optional[AddSharedLinktoaFolderRequestSharedLinkPermissions]):
        unshared_at (Optional[datetime.datetime]): The timestamp at which this shared link will expire. This field can
                only be set by users with paid accounts. The value must be greater than the current date and time.
        vanity_name (Optional[str]): Custom URLs should not be used when sharing sensitive content as vanity URLs are a
                lot easier to guess than regular shared links
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Optional["AddSharedLinktoaFolderRequestSharedLinkAccess"] = Field(
        alias="access", default=None
    )
    password: Optional[str] = Field(alias="password", default=None)
    permissions: Optional["AddSharedLinktoaFolderRequestSharedLinkPermissions"] = Field(
        alias="permissions", default=None
    )
    unshared_at: Optional[datetime.datetime] = Field(alias="unshared_at", default=None)
    vanity_name: Optional[str] = Field(alias="vanity_name", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["AddSharedLinktoaFolderRequestSharedLink"], src_dict: Dict[str, Any]
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
