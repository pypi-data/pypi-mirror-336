"""
Lambda Cloud Python Client

A Python client for interacting with the Lambda Cloud API.
"""

from .client import LambdaCloudClient
from .filesystems import FilesystemAPI
from .firewall import FirewallAPI
from .images import ImageAPI
from .instances import InstanceAPI
from .models import *
from .ssh_keys import SSHKeyAPI

__all__ = ["LambdaCloudClient", "InstanceAPI", "SSHKeyAPI", "FilesystemAPI", "ImageAPI", "FirewallAPI"]

# Version of the lambda_cloud package
__version__ = "0.1.0"
