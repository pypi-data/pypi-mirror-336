from typing import Any, Dict, List, Optional

from .client import LambdaCloudClient


class Instances:
    """Operations related to Lambda Cloud instances.

    This class provides methods for listing, retrieving, launching, restarting,
    and terminating Lambda Cloud instances.
    """

    def __init__(self, client: LambdaCloudClient):
        """Initialize the Instances endpoint group.

        Args:
            client: The Lambda Cloud API client
        """
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """List all running instances.

        Retrieves a list of your running Lambda Cloud instances.

        Returns:
            A list of instance objects

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> instances = Instances(client)
            >>> all_instances = instances.list()
            >>> for instance in all_instances:
            ...     print(f"Instance {instance['id']}: {instance['name']} ({instance['status']})")
        """
        response = self._client._request("GET", "/api/v1/instances")
        return response.get("data", [])

    def get(self, instance_id: str) -> Dict[str, Any]:
        """Retrieve details of a specific instance.

        Fetches detailed information about a single Lambda Cloud instance.

        Args:
            instance_id: The unique identifier of the instance to retrieve

        Returns:
            An instance object with detailed information

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> instances = Instances(client)
            >>> instance = instances.get("INSTANCE_ID_STRING")
            >>> print(f"Instance name: {instance['name']}")
            >>> print(f"IP address: {instance['ip']}")
            >>> print(f"Status: {instance['status']}")
        """
        response = self._client._request("GET", f"/api/v1/instances/{instance_id}")
        return response.get("data", {})

    def update(self, instance_id: str, name: str) -> Dict[str, Any]:
        """Update details of a specific instance.

        Currently supports changing the name of the instance.

        Args:
            instance_id: The unique identifier of the instance to update
            name: The new name for the instance

        Returns:
            The updated instance object

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> instances = Instances(client)
            >>> updated_instance = instances.update("INSTANCE_ID_STRING", "New Instance Name")
            >>> print(f"Updated name: {updated_instance['name']}")
        """
        response = self._client._request("POST", f"/api/v1/instances/{instance_id}", json={"name": name})
        return response.get("data", {})

    def launch(
        self,
        region_name: str,
        instance_type_name: str,
        ssh_key_names: List[str],
        name: Optional[str] = None,
        file_system_names: Optional[List[str]] = None,
        image: Optional[Dict[str, str]] = None,
        user_data: Optional[str] = None,
    ) -> Dict[str, List[str]]:
        """Launch one or more Lambda Cloud instances.

        Creates new instances in the specified region with the given configuration.

        Args:
            region_name: The region in which to launch the instance
            instance_type_name: The type of instance to launch
            ssh_key_names: The names of SSH keys to use for access (currently only one key is supported)
            name: Optional name for the instance
            file_system_names: Optional list of file systems to attach (currently only one is supported)
            image: Optional image specification by ID or family, e.g., {"id": "image-id"} or {"family": "image-family"}
            user_data: Optional cloud-init user data for instance configuration (max size: 1MB)

        Returns:
            A dictionary containing the IDs of launched instances

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> instances = Instances(client)
            >>> result = instances.launch(
            ...     region_name="us-west-1",
            ...     instance_type_name="gpu_1x_a10",
            ...     ssh_key_names=["my-ssh-key"],
            ...     name="ML Training Instance"
            ... )
            >>> print(f"Launched instance IDs: {result['instance_ids']}")
        """
        payload = {
            "region_name": region_name,
            "instance_type_name": instance_type_name,
            "ssh_key_names": ssh_key_names,
            "file_system_names": file_system_names or [],
        }

        if name is not None:
            payload["name"] = name

        if image is not None:
            payload["image"] = image

        if user_data is not None:
            payload["user_data"] = user_data

        response = self._client._request("POST", "/api/v1/instance-operations/launch", json=payload)
        return response.get("data", {})

    def restart(self, instance_ids: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Restart one or more instances.

        Performs a soft restart of the specified instances.

        Args:
            instance_ids: List of instance IDs to restart

        Returns:
            A dictionary containing details of the restarted instances

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> instances = Instances(client)
            >>> result = instances.restart(["INSTANCE_ID_STRING"])
            >>> for instance in result['restarted_instances']:
            ...     print(f"Restarted: {instance['id']} ({instance['status']})")
        """
        response = self._client._request(
            "POST", "/api/v1/instance-operations/restart", json={"instance_ids": instance_ids}
        )
        return response.get("data", {})

    def terminate(self, instance_ids: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Terminate one or more instances.

        Completely shuts down and removes the specified instances.

        Args:
            instance_ids: List of instance IDs to terminate

        Returns:
            A dictionary containing details of the terminated instances

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> instances = Instances(client)
            >>> result = instances.terminate(["INSTANCE_ID_STRING"])
            >>> for instance in result['terminated_instances']:
            ...     print(f"Terminated: {instance['id']} (new status: {instance['status']})")
        """
        response = self._client._request(
            "POST", "/api/v1/instance-operations/terminate", json={"instance_ids": instance_ids}
        )
        return response.get("data", {})
