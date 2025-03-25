# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avoma', 'avoma.api', 'avoma.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.9.3,<4.0.0',
 'email-validator>=2.1.0,<3.0.0',
 'pydantic>=2.6.1,<3.0.0',
 'urllib3>=2.0.0,<3.0.0',
 'yarl>=1.9.4,<2.0.0']

setup_kwargs = {
    'name': 'avoma-client',
    'version': '0.1.3',
    'description': 'An unofficial Python client for the Avoma API',
    'long_description': '# Avoma Python Client\n\nAn unofficial async Python client for the [Avoma API](https://api.avoma.com/docs).\n\n## Installation\n\n```bash\npip install avoma-client\n```\n\nOr with Poetry:\n\n```bash\npoetry add avoma-client\n```\n\n## Usage\n\n```python\nimport asyncio\nfrom avoma import AvomaClient\nfrom datetime import datetime, timedelta\n\nasync def main():\n    # Initialize the client with your API key\n    client = AvomaClient("your-api-key")\n\n    # Get meetings from the last 7 days\n    now = datetime.utcnow()\n    seven_days_ago = now - timedelta(days=7)\n\n    meetings = await client.meetings.list(\n        from_date=seven_days_ago.isoformat(),\n        to_date=now.isoformat()\n    )\n\n    for meeting in meetings.results:\n        print(f"Meeting: {meeting.subject} at {meeting.start_at}")\n\n        # Get meeting insights if available\n        if meeting.state == "completed":\n            insights = await client.meetings.get_insights(meeting.uuid)\n            print(f"Meeting insights: {insights}")\n\nasyncio.run(main())\n```\n\n## Logging\n\nThe client includes built-in logging functionality. You can configure logging directly through the client:\n\n```python\nimport logging\nfrom avoma import AvomaClient\n\n# Set log level directly in the client constructor\nclient = AvomaClient(\n    api_key="your-api-key",\n    log_level=logging.DEBUG,\n    logger_name="my-app.avoma"  # Optional custom logger name\n)\n```\n\nFor more advanced logging configuration:\n\n```python\nimport logging\nimport sys\nfrom avoma import AvomaClient, create_logger\n\n# Create a client with custom logging\nclient = AvomaClient("your-api-key", log_level=logging.DEBUG)\n\n# Customize the logger with a specific handler if needed\nhandler = logging.FileHandler("avoma.log")\nhandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))\n\n# Replace default handler with custom one\nfor h in client.logger.handlers:\n    client.logger.removeHandler(h)\nclient.logger.addHandler(handler)\n```\n\nThe logs include:\n\n- API request and response details (with sensitive data redacted)\n- Client lifecycle events\n- API call information\n\nThis is useful for debugging API interactions and understanding the client\'s behavior.\n\n## Features\n\n- Fully async API using aiohttp\n- Type hints and Pydantic models for all responses\n- Comprehensive test coverage\n- Detailed logging for debugging\n- Support for all Avoma API endpoints:\n  - Meetings\n  - Recordings\n  - Transcriptions\n  - Smart Categories\n  - Templates\n  - Notes\n  - Meeting Sentiments\n  - Users\n  - Calls\n  - Scorecards\n  - Webhooks\n\n## Development\n\n1. Clone the repository\n2. Install dependencies:\n\n```bash\npoetry install\n```\n\n3. Run tests:\n\n```bash\npoetry run pytest\n```\n\n## Contributing\n\nContributions are welcome! Please feel free to submit a Pull Request.\n\n## License\n\nMIT License\n',
    'author': 'Oz Tamir',
    'author_email': 'oz@atamir.fun',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/oztamir/avoma-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
