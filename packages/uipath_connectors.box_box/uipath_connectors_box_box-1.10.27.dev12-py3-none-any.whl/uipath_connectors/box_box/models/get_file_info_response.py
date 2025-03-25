from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_file_info_response_created_by import GetFileInfoResponseCreatedBy
from ..models.get_file_info_response_file_version import GetFileInfoResponseFileVersion
from ..models.get_file_info_response_item_status import GetFileInfoResponseItemStatus
from ..models.get_file_info_response_modified_by import GetFileInfoResponseModifiedBy
from ..models.get_file_info_response_owned_by import GetFileInfoResponseOwnedBy
from ..models.get_file_info_response_parent import GetFileInfoResponseParent
from ..models.get_file_info_response_path_collection import (
    GetFileInfoResponsePathCollection,
)
from ..models.get_file_info_response_shared_link import GetFileInfoResponseSharedLink
from ..models.get_file_info_response_type import GetFileInfoResponseType
import datetime


class GetFileInfoResponse(BaseModel):
    """
    Attributes:
        content_created_at (Optional[datetime.datetime]): The date and time at which this file was originally
                created, which might be before it was uploaded to Box.
        content_modified_at (Optional[datetime.datetime]): The date and time at which this file was last updated,
                which might be before it was uploaded to Box.
        created_at (Optional[datetime.datetime]): The date and time when the file was created on Box.
        created_by (Optional[GetFileInfoResponseCreatedBy]):
        description (Optional[str]): The optional description of this file
        etag (Optional[str]): The HTTP `etag` of this file. This can be used within some API
                endpoints in the `If-Match` and `If-None-Match` headers to only
                perform changes on the file if (no) changes have happened.
        file_version (Optional[GetFileInfoResponseFileVersion]):
        id (Optional[str]): The unique identifier that represent a file.

                The ID for any file can be determined
                by visiting a file in the web application
                and copying the ID from the URL. For example,
                for the URL `https://*.app.box.com/files/123`
                the `file_id` is `123`.
        item_status (Optional[GetFileInfoResponseItemStatus]): Defines if this item has been deleted or not.

                * `active` when the item has is not in the trash
                * `trashed` when the item has been moved to the trash but not deleted
                * `deleted` when the item has been permanently deleted.
        modified_at (Optional[datetime.datetime]): The date and time when the file was last updated on Box.
        modified_by (Optional[GetFileInfoResponseModifiedBy]):
        name (Optional[str]): The name of the file
        owned_by (Optional[GetFileInfoResponseOwnedBy]):
        parent (Optional[GetFileInfoResponseParent]):
        path_collection (Optional[GetFileInfoResponsePathCollection]):
        purged_at (Optional[datetime.datetime]): The time at which this file is expected to be purged
                from the trash.
        sha1 (Optional[str]): The SHA1 hash of the file. This can be used to compare the contents
                of a file on Box with a local file.
        shared_link (Optional[GetFileInfoResponseSharedLink]):
        size (Optional[int]): The file size in bytes. Be careful parsing this integer as it can
                get very large and cause an integer overflow.
        trashed_at (Optional[datetime.datetime]): The time at which this file was put in the trash.
        type_ (Optional[GetFileInfoResponseType]): `file`
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    content_created_at: Optional[datetime.datetime] = Field(
        alias="content_created_at", default=None
    )
    content_modified_at: Optional[datetime.datetime] = Field(
        alias="content_modified_at", default=None
    )
    created_at: Optional[datetime.datetime] = Field(alias="created_at", default=None)
    created_by: Optional["GetFileInfoResponseCreatedBy"] = Field(
        alias="created_by", default=None
    )
    description: Optional[str] = Field(alias="description", default=None)
    etag: Optional[str] = Field(alias="etag", default=None)
    file_version: Optional["GetFileInfoResponseFileVersion"] = Field(
        alias="file_version", default=None
    )
    id: Optional[str] = Field(alias="id", default=None)
    item_status: Optional["GetFileInfoResponseItemStatus"] = Field(
        alias="item_status", default=None
    )
    modified_at: Optional[datetime.datetime] = Field(alias="modified_at", default=None)
    modified_by: Optional["GetFileInfoResponseModifiedBy"] = Field(
        alias="modified_by", default=None
    )
    name: Optional[str] = Field(alias="name", default=None)
    owned_by: Optional["GetFileInfoResponseOwnedBy"] = Field(
        alias="owned_by", default=None
    )
    parent: Optional["GetFileInfoResponseParent"] = Field(alias="parent", default=None)
    path_collection: Optional["GetFileInfoResponsePathCollection"] = Field(
        alias="path_collection", default=None
    )
    purged_at: Optional[datetime.datetime] = Field(alias="purged_at", default=None)
    sha1: Optional[str] = Field(alias="sha1", default=None)
    shared_link: Optional["GetFileInfoResponseSharedLink"] = Field(
        alias="shared_link", default=None
    )
    size: Optional[int] = Field(alias="size", default=None)
    trashed_at: Optional[datetime.datetime] = Field(alias="trashed_at", default=None)
    type_: Optional["GetFileInfoResponseType"] = Field(alias="type", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetFileInfoResponse"], src_dict: Dict[str, Any]):
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
