from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from .common import PublicRegionCode, Region


class UserStatus(str, Enum):
    """Status of the user's account."""

    ACTIVE = "active"
    DEACTIVATED = "deactivated"


class User(BaseModel):
    """Information about a user in your Team."""

    id: str = Field(..., description="The unique identifier for the user.")
    email: str = Field(..., description="The email address of the user.")
    status: UserStatus = Field(..., description="The status of the user's account.")


class Filesystem(BaseModel):
    """Information about a shared filesystem."""

    id: str = Field(..., description="The unique identifier (ID) of the filesystem.")
    name: str = Field(..., description="The name of the filesystem.")
    mount_point: str = Field(
        ..., description="The absolute path indicating where on instances the filesystem will be mounted."
    )
    created: datetime = Field(
        ..., description="The date and time at which the filesystem was created. Formatted as an ISO 8601 timestamp."
    )
    created_by: User = Field(..., description="The user in your Team that created the filesystem.")
    is_in_use: bool = Field(
        ...,
        description="Whether the filesystem is currently in use by an instance. Filesystems that are in use cannot be deleted.",
    )
    region: Region = Field(..., description="The region in which the filesystem is deployed.")
    bytes_used: Optional[int] = Field(
        None,
        description="The approximate amount of storage used by the filesystem in bytes. This estimate is updated every few hours.",
    )


class FilesystemCreateRequest(BaseModel):
    """Request to create a new filesystem."""

    name: str = Field(
        ..., min_length=1, max_length=60, pattern=r"^[a-zA-Z]+[0-9a-zA-Z-]*$", description="The name of the filesystem."
    )
    region: PublicRegionCode = Field(..., description="The region in which you want to create the filesystem.")


class FilesystemDeleteResponse(BaseModel):
    """Response after deleting a filesystem."""

    deleted_ids: List[str] = Field(..., description="The unique identifiers of the filesystems that were deleted.")
