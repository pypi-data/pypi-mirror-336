from typing import Any, Dict, List

from .client import LambdaCloudClient


class Filesystems:
    """Operations related to filesystems in Lambda Cloud.

    This class provides methods for listing, creating, and deleting filesystems
    that can be attached to instances.
    """

    def __init__(self, client: LambdaCloudClient):
        """Initialize the Filesystems endpoint group.

        Args:
            client: The Lambda Cloud API client
        """
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """List all filesystems in your account.

        Retrieves a list of all filesystems owned by your Lambda Cloud account.

        Returns:
            A list of filesystem objects

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> filesystems = Filesystems(client)
            >>> fs_list = filesystems.list()
            >>> for fs in fs_list:
            ...     in_use = "in use" if fs["is_in_use"] else "not in use"
            ...     print(f"Filesystem: {fs['name']} ({in_use}, {fs['region']['name']})")
        """
        response = self._client._request("GET", "/api/v1/file-systems")
        return response.get("data", [])

    def create(self, name: str, region: str) -> Dict[str, Any]:
        """Create a new filesystem.

        Creates a new filesystem in the specified region that can be attached to instances.

        Args:
            name: Name for the filesystem (must start with a letter and contain only alphanumeric characters and hyphens)
            region: Region code where the filesystem should be created

        Returns:
            A filesystem object

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> filesystems = Filesystems(client)
            >>> new_fs = filesystems.create("my-data", "us-west-1")
            >>> print(f"Created filesystem: {new_fs['name']} (ID: {new_fs['id']})")
            >>> print(f"Mount point: {new_fs['mount_point']}")
        """
        response = self._client._request("POST", "/api/v1/filesystems", json={"name": name, "region": region})
        return response.get("data", {})

    def delete(self, filesystem_id: str) -> Dict[str, List[str]]:
        """Delete a filesystem.

        Deletes the specified filesystem. The filesystem must not be attached to any instances.

        Args:
            filesystem_id: The ID of the filesystem to delete

        Returns:
            A dictionary containing the IDs of deleted filesystems

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> filesystems = Filesystems(client)
            >>> result = filesystems.delete("398578a2336b49079e74043f0bd2cfe8")
            >>> print(f"Deleted filesystem IDs: {result['deleted_ids']}")
        """
        response = self._client._request("DELETE", f"/api/v1/filesystems/{filesystem_id}")
        return response.get("data", {})
