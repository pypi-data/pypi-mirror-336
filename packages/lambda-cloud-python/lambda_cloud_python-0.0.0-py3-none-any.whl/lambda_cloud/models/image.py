from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from .common import Region


class ImageArchitecture(str, Enum):
    """CPU architecture supported by an image."""

    X86_64 = "x86_64"
    ARM64 = "arm64"


class Image(BaseModel):
    """An available machine image in Lambda Cloud."""

    id: str = Field(..., description="The unique identifier (ID) for an image.")
    created_time: datetime = Field(..., description="The date and time that the image was created.")
    updated_time: datetime = Field(..., description="The date and time that the image was last updated.")
    name: str = Field(..., description="The human-readable identifier for an image.")
    description: str = Field(..., description="Additional information about the image.")
    family: str = Field(..., description="The family the image belongs to.")
    version: str = Field(..., description="The image version.")
    architecture: ImageArchitecture = Field(..., description="The CPU architecture the image supports.")
    region: Region = Field(..., description="The region in which this image is available.")
