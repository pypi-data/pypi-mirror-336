from typing import Optional

from pydantic import BaseModel, Field


class ApiErrorUnauthorized(BaseModel):
    """Error returned when authentication fails."""

    code: str = Field("global/invalid-api-key", description="The unique identifier for the type of error.")
    message: str = Field("API key was invalid, expired, or deleted.", description="A description of the error.")
    suggestion: str = Field(
        "Check your API key or create a new one, then try again.",
        description="One or more suggestions of possible ways to fix the error.",
    )


class ApiErrorAccountInactive(BaseModel):
    """Error returned when the account is inactive."""

    code: str = Field("global/account-inactive", description="The unique identifier for the type of error.")
    message: str = Field("Your account is inactive.", description="A description of the error.")
    suggestion: str = Field(
        "Make sure you have verified your email address and have a valid payment method. Contact Support if problems continue.",
        description="One or more suggestions of possible ways to fix the error.",
    )


class ApiErrorInstanceNotFound(BaseModel):
    """Error returned when an instance cannot be found."""

    code: str = Field("global/object-does-not-exist", description="The unique identifier for the type of error.")
    message: str = Field("Specified instance does not exist.", description="A description of the error.")
    suggestion: Optional[str] = Field(None, description="One or more suggestions of possible ways to fix the error.")


class ApiErrorInvalidParameters(BaseModel):
    """Error returned when request parameters are invalid."""

    code: str = Field("global/invalid-parameters", description="The unique identifier for the type of error.")
    message: str = Field("Invalid request data.", description="A description of the error.")
    suggestion: Optional[str] = Field(None, description="One or more suggestions of possible ways to fix the error.")


class ApiErrorInvalidBillingAddress(BaseModel):
    """Error returned when billing address is invalid."""

    code: str = Field("global/invalid-address", description="The unique identifier for the type of error.")
    message: str = Field("Your billing address is invalid.", description="A description of the error.")
    suggestion: str = Field(
        "Make sure your billing address is valid. Contact Support if problems continue.",
        description="One or more suggestions of possible ways to fix the error.",
    )


class ApiErrorFileSystemInWrongRegion(BaseModel):
    """Error returned when a filesystem is in a different region than requested."""

    code: str = Field(
        "instance-operations/launch/file-system-in-wrong-region",
        description="The unique identifier for the type of error.",
    )
    message: str = Field(..., description="A description of the error.")
    suggestion: Optional[str] = Field(None, description="One or more suggestions of possible ways to fix the error.")


class ApiErrorInsufficientCapacity(BaseModel):
    """Error returned when there is not enough capacity to fulfill request."""

    code: str = Field(
        "instance-operations/launch/insufficient-capacity", description="The unique identifier for the type of error."
    )
    message: str = Field("Not enough capacity to fulfill launch request.", description="A description of the error.")
    suggestion: Optional[str] = Field(None, description="One or more suggestions of possible ways to fix the error.")


class ApiErrorLaunchResourceNotFound(BaseModel):
    """Error returned when a resource needed for launch cannot be found."""

    code: str = Field("global/object-does-not-exist", description="The unique identifier for the type of error.")
    message: str = Field(..., description="The resource the API was unable to find.")
    suggestion: str = Field(..., description="One or more suggestions of possible ways to fix the error.")


class ApiErrorQuotaExceeded(BaseModel):
    """Error returned when a quota has been exceeded."""

    code: str = Field("global/quota-exceeded", description="The unique identifier for the type of error.")
    message: str = Field("Quota exceeded.", description="A description of the error.")
    suggestion: str = Field(
        "Contact Support to increase your quota.",
        description="One or more suggestions of possible ways to fix the error.",
    )


class ApiErrorDuplicate(BaseModel):
    """Error returned when trying to create a duplicate resource."""

    code: str = Field("global/duplicate", description="The unique identifier for the type of error.")
    message: str = Field(..., description="A description of the error.")
    suggestion: Optional[str] = Field(None, description="One or more suggestions of possible ways to fix the error.")


class ApiErrorFilesystemNotFound(BaseModel):
    """Error returned when a filesystem cannot be found."""

    code: str = Field("global/object-does-not-exist", description="The unique identifier for the type of error.")
    message: str = Field("Filesystem was not found.", description="A description of the error.")
    suggestion: Optional[str] = Field(None, description="One or more suggestions of possible ways to fix the error.")


class ApiErrorFilesystemInUse(BaseModel):
    """Error returned when trying to delete a filesystem that is in use."""

    code: str = Field("filesystems/filesystem-in-use", description="The unique identifier for the type of error.")
    message: str = Field(..., description="A description of the error.")
    suggestion: Optional[str] = Field(None, description="One or more suggestions of possible ways to fix the error.")
