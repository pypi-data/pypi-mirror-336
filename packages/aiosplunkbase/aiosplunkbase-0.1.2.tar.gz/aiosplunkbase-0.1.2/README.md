# aiosplunkbase

A simple async API client for interacting with Splunk's Splunkbase service.

## Installation

You can install aiosplunkbase using pip:

```bash
pip install aiosplunkbase
```

## Usage Examples

### Usage

```python
from aiosplunkbase import SBClient
from pprint import pprint

async def main():
    async with SBClient(username="your_username", password="your_password") as client:
        await client.login()

        app_info = await client.get_app_info("Splunk_TA_aws")
        pprint(app_info)

        latest_version = await client.get_app_latest_version(
            "Splunk_TA_aws",
            splunk_version="9.1",
            is_cloud=False
        )
        pprint(latest_version)

        async for chunk in client.download_app("Splunk_TA_aws"):
            pass
```

## License

MIT License