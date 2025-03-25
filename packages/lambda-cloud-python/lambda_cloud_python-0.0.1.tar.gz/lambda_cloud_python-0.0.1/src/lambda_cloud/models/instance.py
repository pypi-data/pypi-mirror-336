from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .common import PublicRegionCode, Region


class InstanceStatus(str, Enum):
    """The current status of an instance."""

    BOOTING = "booting"
    ACTIVE = "active"
    UNHEALTHY = "unhealthy"
    TERMINATED = "terminated"
    TERMINATING = "terminating"


class InstanceTypeSpecs(BaseModel):
    """Technical specifications for an instance type."""

    vcpus: int = Field(..., description="The number of virtual CPUs.")
    memory_gib: int = Field(..., description="The amount of RAM in gibibytes (GiB).")
    storage_gib: int = Field(..., description="The amount of storage in gibibytes (GiB).")
    gpus: int = Field(..., description="The number of GPUs.")


class InstanceType(BaseModel):
    """Detailed information about an instance type."""

    name: str = Field(..., description="The name of the instance type.")
    description: str = Field(..., description="A description of the instance type.")
    gpu_description: str = Field(..., description="The type of GPU used by this instance type.")
    price_cents_per_hour: int = Field(..., description="The price of the instance type in US cents per hour.")
    specs: InstanceTypeSpecs = Field(..., description="Detailed technical specifications for the instance type.")


class InstanceActionUnavailableCode(str, Enum):
    """Possible reasons an action might be unavailable."""

    VM_HAS_NOT_LAUNCHED = "vm-has-not-launched"
    VM_IS_TOO_OLD = "vm-is-too-old"
    VM_IS_TERMINATING = "vm-is-terminating"


class InstanceActionAvailabilityDetails(BaseModel):
    """Details about the availability of an action for an instance."""

    available: bool = Field(
        ...,
        description="If set, indicates that the relevant operation can be performed on the instance in its current state.",
    )
    reason_code: Optional[Union[InstanceActionUnavailableCode, str]] = Field(
        None,
        description="A code representing the instance state that is blocking the operation. Only provided if the operation is blocked.",
    )
    reason_description: Optional[str] = Field(
        None,
        description="A longer description of why this operation is currently blocked. Only provided if the operation is blocked.",
    )


class InstanceActionAvailability(BaseModel):
    """Set of status objects representing the current availability of common instance operations."""

    migrate: InstanceActionAvailabilityDetails = Field(
        ...,
        description="Indicates whether the instance is currently able to be migrated. If not, describes why the operation is blocked.",
    )
    rebuild: InstanceActionAvailabilityDetails = Field(
        ...,
        description="Indicates whether the instance is currently able to be rebuilt. If not, describes why the operation is blocked.",
    )
    restart: InstanceActionAvailabilityDetails = Field(
        ...,
        description="Indicates whether the instance is currently able to be restarted. If not, describes why the operation is blocked.",
    )
    cold_reboot: InstanceActionAvailabilityDetails = Field(
        ...,
        description="Indicates whether the instance is currently eligible for a cold reboot. If not, describes why the operation is blocked.",
    )
    terminate: InstanceActionAvailabilityDetails = Field(
        ...,
        description="Indicates whether the instance is currently able to be terminated. If not, describes why the operation is blocked.",
    )


class Instance(BaseModel):
    """Detailed information about an instance."""

    id: str = Field(..., description="The unique identifier of the instance.")
    name: Optional[str] = Field(None, description="If set, the user-provided name of the instance.")
    ip: Optional[str] = Field(None, description="The public IPv4 address of the instance.")
    private_ip: Optional[str] = Field(None, description="The private IPv4 address of the instance.")
    status: InstanceStatus = Field(..., description="The current status of the instance.")
    ssh_key_names: List[str] = Field(
        ..., description="The names of the SSH keys that are allowed to access the instance."
    )
    file_system_names: List[str] = Field(
        ...,
        description="The names of the filesystems attached to the instance. If no filesystems are attached, this array is empty.",
    )
    region: Region = Field(..., description="The region in which the instance is deployed.")
    instance_type: InstanceType = Field(..., description="Detailed information about the instance's instance type.")
    hostname: Optional[str] = Field(
        None, description="The hostname assigned to this instance, which resolves to the instance's IP."
    )
    jupyter_token: Optional[str] = Field(
        None, description="The secret token used to log into the JupyterLab server hosted on the instance."
    )
    jupyter_url: Optional[str] = Field(
        None, description="The URL that opens the JupyterLab environment on the instance."
    )
    is_reserved: Optional[bool] = Field(None, description="Whether this is a reserved instance.")
    actions: InstanceActionAvailability = Field(
        ..., description="A set of status objects representing the current availability of common instance operations."
    )


class InstanceTypesItem(BaseModel):
    """Information about an instance type and its availability."""

    instance_type: InstanceType = Field(
        ..., description="The description, technical specifications, and metadata for this instance type."
    )
    regions_with_capacity_available: List[Region] = Field(
        ..., description="A list of the regions in which this instance type is available."
    )


class InstanceTypes(BaseModel):
    """A dictionary mapping instance type names to their details and availability."""

    __root__: Dict[str, InstanceTypesItem]


class InstanceModificationRequest(BaseModel):
    """Request to modify an instance's details."""

    name: Optional[str] = Field(None, max_length=64, description="The new, user-provided name for the instance.")


class ImageSpecificationID(BaseModel):
    """Specifies an image to use by its unique identifier."""

    id: str = Field(..., description="The unique identifier of the image.")


class ImageSpecificationFamily(BaseModel):
    """Specifies an image to use by its family name."""

    family: str = Field(..., description="The family name of the image.")


class InstanceLaunchRequest(BaseModel):
    """Request to launch one or more instances."""

    region_name: PublicRegionCode = Field(..., description="The region into which you want to launch the instance.")
    instance_type_name: str = Field(..., description="The type of instance you want to launch.")
    ssh_key_names: List[str] = Field(
        ...,
        description="The names of the SSH keys you want to use to provide access to the instance. Currently, exactly one SSH key must be specified.",
    )
    file_system_names: List[str] = Field(
        default=[],
        description="The names of the filesystems you want to attach to the instance. Currently, you can attach only one filesystem during instance creation. By default, no filesystems are attached.",
    )
    name: Optional[str] = Field(
        None, max_length=64, description="The name you want to assign to your instance. Must be 64 characters or fewer."
    )
    image: Optional[Union[ImageSpecificationID, ImageSpecificationFamily]] = Field(
        None, description="The machine image you want to use. Defaults to the latest Lambda Stack image."
    )
    user_data: Optional[str] = Field(
        None, description="An instance configuration string specified in a valid cloud-init user-data format."
    )


class InstanceLaunchResponse(BaseModel):
    """Response containing the IDs of launched instances."""

    instance_ids: List[str] = Field(..., description="The unique identifiers (IDs) of the launched instances.")


class InstanceRestartRequest(BaseModel):
    """Request to restart one or more instances."""

    instance_ids: List[str] = Field(..., description="The unique identifiers (IDs) of the instances to restart.")


class InstanceRestartResponse(BaseModel):
    """Response containing details of restarted instances."""

    restarted_instances: List[Instance] = Field(
        ..., description="The list of instances that were successfully restarted."
    )


class InstanceTerminateRequest(BaseModel):
    """Request to terminate one or more instances."""

    instance_ids: List[str] = Field(..., description="The unique identifiers (IDs) of the instances to terminate.")


class InstanceTerminateResponse(BaseModel):
    """Response containing details of terminated instances."""

    terminated_instances: List[Instance] = Field(
        ..., description="The list of instances that were successfully terminated."
    )
