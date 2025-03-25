from typing import Any, Dict, List, Optional

from .client import LambdaCloudClient


class SSHKeys:
    """Operations related to SSH keys in Lambda Cloud.

    This class provides methods for listing, adding, and deleting SSH keys
    used for instance authentication.
    """

    def __init__(self, client: LambdaCloudClient):
        """Initialize the SSHKeys endpoint group.

        Args:
            client: The Lambda Cloud API client
        """
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """List all SSH keys in your account.

        Retrieves a list of your SSH keys registered with Lambda Cloud.

        Returns:
            A list of SSH key objects

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> ssh_keys = SSHKeys(client)
            >>> keys = ssh_keys.list()
            >>> for key in keys:
            ...     print(f"Key: {key['name']} (ID: {key['id']})")
        """
        response = self._client._request("GET", "/api/v1/ssh-keys")
        return response.get("data", [])

    def add(self, name: str, public_key: Optional[str] = None) -> Dict[str, Any]:
        """Add a new SSH key to your account.

        You can either upload an existing public key or generate a new key pair.
        If public_key is provided, it will be used; otherwise, a new key pair will
        be generated and the private key will be returned (but not stored by Lambda).

        Args:
            name: A name for the SSH key
            public_key: Optional public key to upload. If not provided, a new key pair will be generated.

        Returns:
            An SSH key object (with private_key if generated)

        Examples:
            # Adding an existing key:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> ssh_keys = SSHKeys(client)
            >>> with open("~/.ssh/id_ed25519.pub", "r") as f:
            ...     public_key_content = f.read().strip()
            >>> key = ssh_keys.add("my-laptop-key", public_key=public_key_content)
            >>> print(f"Added key: {key['name']} (ID: {key['id']})")

            # Generating a new key:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> ssh_keys = SSHKeys(client)
            >>> key = ssh_keys.add("new-generated-key")
            >>> print(f"Generated key: {key['name']} (ID: {key['id']})")
            >>> # Save the private key locally
            >>> with open("new_key.pem", "w") as f:
            ...     f.write(key['private_key'])
            >>> print("Private key saved to new_key.pem")
        """
        payload = {"name": name}
        if public_key is not None:
            payload["public_key"] = public_key

        response = self._client._request("POST", "/api/v1/ssh-keys", json=payload)
        return response.get("data", {})

    def delete(self, key_id: str) -> Dict[str, Any]:
        """Delete an SSH key.

        Removes the specified SSH key from your Lambda Cloud account.

        Args:
            key_id: The ID of the SSH key to delete

        Returns:
            An empty dictionary on success

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> ssh_keys = SSHKeys(client)
            >>> ssh_keys.delete("A_KEY_ID")
            >>> print("SSH key deleted successfully")
        """
        response = self._client._request("DELETE", f"/api/v1/ssh-keys/{key_id}")
        return response.get("data", {})
