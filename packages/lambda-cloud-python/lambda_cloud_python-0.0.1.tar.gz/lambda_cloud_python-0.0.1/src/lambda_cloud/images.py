from typing import Any, Dict, List

from .client import LambdaCloudClient


class Images:
    """Operations related to machine images in Lambda Cloud.

    This class provides methods for listing available machine images.
    """

    def __init__(self, client: LambdaCloudClient):
        """Initialize the Images endpoint group.

        Args:
            client: The Lambda Cloud API client
        """
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """List available machine images.

        Retrieves a list of available machine images that can be used when launching instances.

        Returns:
            A list of image objects

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> images = Images(client)
            >>> available_images = images.list()
            >>> for img in available_images:
            ...     print(f"Image: {img['name']} (Family: {img['family']}, Region: {img['region']['name']})")
        """
        response = self._client._request("GET", "/api/v1/images")
        return response.get("data", [])
