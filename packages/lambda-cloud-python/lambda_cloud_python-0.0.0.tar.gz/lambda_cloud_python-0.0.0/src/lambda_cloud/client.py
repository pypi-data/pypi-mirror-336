from typing import Any, Dict, Optional

import httpx


class LambdaCloudClient:
    """Base client for the Lambda Cloud API.

    Handles authentication and provides common HTTP functionality for Lambda Cloud API requests.

    Attributes:
        api_key (str): Your Lambda Cloud API key
        base_url (str): The base URL for the Lambda Cloud API
        client (httpx.Client): HTTP client for making requests
    """

    def __init__(self, api_key: str, base_url: str = "https://cloud.lambdalabs.com", timeout: int = 60):
        """Initialize a new Lambda Cloud API client.

        Args:
            api_key: Your Lambda Cloud API key
            base_url: The base URL for the Lambda Cloud API (default: https://cloud.lambdalabs.com)
            timeout: Request timeout in seconds (default: 60)

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
        """
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
        )

    def _request(
        self, method: str, path: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Lambda Cloud API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Query parameters to include in the request
            json: JSON body to include in the request

        Returns:
            The parsed JSON response data

        Raises:
            httpx.HTTPError: If the request fails
        """
        response = self.client.request(method=method, url=path, params=params, json=json)
        response.raise_for_status()
        return response.json()

    def close(self):
        """Close the HTTP client session."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
