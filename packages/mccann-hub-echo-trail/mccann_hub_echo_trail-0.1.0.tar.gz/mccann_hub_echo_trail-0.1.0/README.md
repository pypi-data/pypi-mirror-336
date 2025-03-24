# Echo Trail

A JSON logger with dynamic metadata injection for consistent log formatting across projects.

## Features

- JSON log formatting for improved log readability.
- Metadata injection, including hostname, program name, and custom fields.
- Supports both console and rotating file handlers by default.

## Installation

```bash
pip install mccann_hub_echo_trail
```

## Usage

```python
from mccann_hub.echo_trail import logger_setup, get_logger

def main():
  logger = get_logger(__name__)
  logger.info("Hello world!")

if __name__ == "__main__":
  logger_setup()
  main()
```

## License

This project is licensed under the MIT License.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
