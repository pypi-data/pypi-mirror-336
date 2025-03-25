from typing import Any, Dict

from .client import LambdaCloudClient


class InstanceTypes:
    """Operations related to Lambda Cloud instance types.

    This class provides methods for listing available instance types.
    """

    def __init__(self, client: LambdaCloudClient):
        """Initialize the InstanceTypes endpoint group.

        Args:
            client: The Lambda Cloud API client
        """
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List available instance types.

        Retrieves a list of the instance types currently offered on Lambda's public cloud,
        along with details about each type including resource specifications, pricing,
        and regional availability.

        Returns:
            A dictionary mapping instance type names to their details

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> instance_types = InstanceTypes(client)
            >>> available_types = instance_types.list()
            >>> for type_name, details in available_types.items():
            ...     specs = details['instance_type']['specs']
            ...     price = details['instance_type']['price_cents_per_hour'] / 100
            ...     print(f"{type_name}: {specs['gpus']}x GPU, {specs['memory_gib']} GiB RAM, ${price}/hr")
            ...     print(f"  Available in regions: {[r['name'] for r in details['regions_with_capacity_available']]}")
        """
        response = self._client._request("GET", "/api/v1/instance-types")
        return response.get("data", {})
