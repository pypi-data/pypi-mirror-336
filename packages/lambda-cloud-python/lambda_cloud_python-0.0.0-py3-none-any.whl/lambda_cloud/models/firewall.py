import ipaddress
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class SecurityGroupRuleProtocol(str, Enum):
    """Network protocols that can be specified in firewall rules."""

    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ALL = "all"


class FirewallRule(BaseModel):
    """A rule that controls inbound network traffic to instances."""

    protocol: SecurityGroupRuleProtocol = Field(..., description="The protocol to which the rule applies.")
    port_range: Optional[List[int]] = Field(
        None,
        min_items=2,
        max_items=2,
        description="An inclusive range of network ports specified as [min, max]. Not allowed for the icmp protocol but required for the others.",
    )
    source_network: str = Field(
        ...,
        description="The set of source IPv4 addresses from which you want to allow inbound traffic. These addresses must be specified in CIDR notation.",
    )
    description: str = Field(..., max_length=128, description="A human-readable description of the rule.")

    @field_validator("port_range")
    def validate_port_range(cls, v, values):
        if "protocol" in values and values["protocol"] == SecurityGroupRuleProtocol.ICMP and v is not None:
            raise ValueError("port_range should not be specified for ICMP protocol")
        if "protocol" in values and values["protocol"] != SecurityGroupRuleProtocol.ICMP and (v is None or len(v) != 2):
            raise ValueError("port_range is required for non-ICMP protocols and must contain exactly 2 items")
        if v and (v[0] < 1 or v[0] > 65535 or v[1] < 1 or v[1] > 65535):
            raise ValueError("port values must be between 1 and 65535")
        if v and v[0] > v[1]:
            raise ValueError("the first port value must be less than or equal to the second port value")
        return v

    @field_validator("source_network")
    def validate_source_network(cls, v):
        try:
            # If only an IP address is provided (without a mask), assume /32
            if "/" not in v:
                v = f"{v}/32"
            ipaddress.IPv4Network(v)
            return v
        except ValueError:
            raise ValueError("source_network must be a valid IPv4 CIDR block")


class FirewallRulesPutRequest(BaseModel):
    """Request to replace all inbound firewall rules."""

    data: List[FirewallRule] = Field(..., description="The list of inbound firewall rules.")
