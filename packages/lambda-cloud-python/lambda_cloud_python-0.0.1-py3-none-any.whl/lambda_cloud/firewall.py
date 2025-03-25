from typing import Any, Dict, List

from .client import LambdaCloudClient


class FirewallRules:
    """Operations related to firewall rules in Lambda Cloud.

    This class provides methods for listing and updating firewall rules
    that control inbound traffic to your instances.

    Note: Firewall rules do not apply to the us-south-1 region.
    """

    def __init__(self, client: LambdaCloudClient):
        """Initialize the FirewallRules endpoint group.

        Args:
            client: The Lambda Cloud API client
        """
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """List inbound firewall rules.

        Retrieves a list of your inbound firewall rules.

        Returns:
            A list of firewall rule objects

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> firewall = FirewallRules(client)
            >>> rules = firewall.list()
            >>> for rule in rules:
            ...     port_range = f"{rule['port_range'][0]}-{rule['port_range'][1]}" if 'port_range' in rule else "N/A"
            ...     print(f"Rule: {rule['protocol']} {port_range} from {rule['source_network']} ({rule['description']})")
        """
        response = self._client._request("GET", "/api/v1/firewall-rules")
        return response.get("data", [])

    def replace(self, rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Replace all inbound firewall rules.

        Overwrites the current set of inbound firewall rules with the provided rules.

        Note: This replaces ALL existing rules with the new set.

        Args:
            rules: List of firewall rule objects. Each rule should have:
                - protocol: 'tcp', 'udp', 'icmp', or 'all'
                - port_range: [min_port, max_port] (required for tcp, udp, all)
                - source_network: CIDR notation for source IPs (e.g., '0.0.0.0/0')
                - description: Human-readable description of the rule

        Returns:
            The new list of firewall rule objects

        Examples:
            >>> client = LambdaCloudClient(api_key="your-api-key")
            >>> firewall = FirewallRules(client)
            >>> new_rules = [
            ...     {
            ...         "protocol": "tcp",
            ...         "port_range": [22, 22],
            ...         "source_network": "0.0.0.0/0",
            ...         "description": "Allow SSH from anywhere"
            ...     },
            ...     {
            ...         "protocol": "tcp",
            ...         "port_range": [80, 80],
            ...         "source_network": "0.0.0.0/0",
            ...         "description": "Allow HTTP from anywhere"
            ...     }
            ... ]
            >>> updated_rules = firewall.replace(new_rules)
            >>> print(f"Updated with {len(updated_rules)} rules")
        """
        response = self._client._request("PUT", "/api/v1/firewall-rules", json={"data": rules})
        return response.get("data", [])
