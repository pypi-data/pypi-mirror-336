from typing import Optional

from pydantic import BaseModel, Field


class SSHKey(BaseModel):
    """Information about a stored SSH key, which can be used to access instances over SSH."""

    id: str = Field(..., description="The unique identifier (ID) of the SSH key.")
    name: str = Field(..., min_length=1, max_length=64, description="The name of the SSH key.")
    public_key: str = Field(..., min_length=1, max_length=4096, description="The public key for the SSH key.")


class GeneratedSSHKey(SSHKey):
    """Information about a server-generated SSH key, which can be used to access instances over SSH."""

    private_key: str = Field(
        ...,
        description="The private key generated in the SSH key pair. Make sure to store a copy of this key locally, as Lambda does not store the key server-side.",
    )


class AddSSHKeyRequest(BaseModel):
    """Request to add an SSH key."""

    name: str = Field(..., min_length=1, max_length=64, description="The name of the SSH key.")
    public_key: Optional[str] = Field(
        None,
        min_length=1,
        max_length=4096,
        description="The public key for the SSH key. If not provided, a new key pair will be generated.",
    )
