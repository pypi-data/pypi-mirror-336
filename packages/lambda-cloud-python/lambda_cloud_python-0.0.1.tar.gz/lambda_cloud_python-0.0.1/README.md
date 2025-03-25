# Lambda Cloud Python

A simple Python client for the [Lambda Cloud API](https://cloud.lambdalabs.com/api/v1/docs#overview--response-types-and-formats), built with [httpx](https://www.python-httpx.org/).

## Installation

### Installation via PyPI

```bash
pip install lambda-cloud-python
```

### Installation from source

```bash
git clone https://github.com/jxtngx/lambda-cloud-python.git
cd lambda-cloud-python
pip install -e .
```

## Usage

> [!NOTE]
> see [docs](./docs/) for more examples

The Lambda Cloud Python client provides the following functionality:

### Instances
- `instances.list()` - Get all instances for the account
- `instances.get(instance_id)` - Get details for a specific instance
- `instances.update(instance_id, ...)` - Update details of a specific instance
- `instances.launch(...)` - Launch one or more new instances
- `instances.restart(instance_ids)` - Start one or more instances
- `instances.terminate(instance_ids)` - Terminate one or more instances

### Instance Types
- `instance_types.list()` - Get available instance types and their specifications

### SSH Keys
- `ssh_keys.list()` - Get all SSH keys for the account
- `ssh_keys.add(name, public_key)` - Add a new SSH key
- `ssh_keys.delete(name)` - Delete an SSH key

### File Systems
- `file_systems.list()` - Get all file systems for the account
- `file_systems.create(...)` - Create a new file system
- `file_systems.delete(name)` - Delete a file system

### Images
- `images.list()` - List available machine images
