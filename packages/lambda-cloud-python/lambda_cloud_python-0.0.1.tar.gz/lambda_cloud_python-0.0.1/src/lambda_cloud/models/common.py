from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PublicRegionCode(str, Enum):
    """Available region codes for Lambda Cloud services."""

    EUROPE_CENTRAL_1 = "europe-central-1"
    ASIA_SOUTH_1 = "asia-south-1"
    AUSTRALIA_EAST_1 = "australia-east-1"
    ME_WEST_1 = "me-west-1"
    ASIA_NORTHEAST_1 = "asia-northeast-1"
    ASIA_NORTHEAST_2 = "asia-northeast-2"
    US_EAST_1 = "us-east-1"
    US_WEST_2 = "us-west-2"
    US_WEST_1 = "us-west-1"
    US_SOUTH_1 = "us-south-1"
    US_WEST_3 = "us-west-3"
    US_MIDWEST_1 = "us-midwest-1"
    US_EAST_2 = "us-east-2"
    US_SOUTH_2 = "us-south-2"
    US_SOUTH_3 = "us-south-3"
    US_EAST_3 = "us-east-3"
    US_MIDWEST_2 = "us-midwest-2"
    TEST_EAST_1 = "test-east-1"
    TEST_WEST_1 = "test-west-1"


class Region(BaseModel):
    """A region in which Lambda Cloud resources can be deployed."""

    name: PublicRegionCode = Field(..., description="The region code.")
    description: str = Field(..., description="The location represented by the region code.")


class EmptyResponse(BaseModel):
    """An empty response returned by some API endpoints."""

    pass


class ResponseWrapper(BaseModel):
    """Generic wrapper for successful API responses."""

    data: Any = Field(..., description="The response data.")


class ErrorResponseWrapper(BaseModel):
    """Generic wrapper for error API responses."""

    error: Any = Field(..., description="The error details.")
