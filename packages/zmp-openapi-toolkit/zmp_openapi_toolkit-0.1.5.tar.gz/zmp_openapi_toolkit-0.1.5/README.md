# zmp-openapi-toolkit

![Platform Badge](https://img.shields.io/badge/platform-zmp-red)
![Component Badge](https://img.shields.io/badge/component-toolkit-red)
![CI Badge](https://img.shields.io/badge/ci-github_action-green)
![License Badge](https://img.shields.io/badge/license-MIT-green)
![PyPI - Version](https://img.shields.io/pypi/v/zmp-openapi-toolkit)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/zmp-openapi-toolkit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zmp-openapi-toolkit)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/zmp-openapi-toolkit)

## Introduction

This is a toolkit library for the LLM application using the multiple openapi specifications

## Key Features

- Support the OpenAPI request wrapper
- OpenAPI parameters and request type validation
- Convenient authentication management

## Installation

Install using pip:

```bash
pip install zmp-openapi-toolkit
```

Install using poetry:
```bash
poetry add zmp-openapi-toolkit
```

## Usage

Basic example:

```python
import logging
import logging.config
from typing import List

from zmp_openapi_toolkit import (
    MixedAPISpecConfig,
    ZmpAPIWrapper,
    ZmpTool,
    ZmpToolkit,
)

logging.getLogger("zmp_openapi_toolkit.openapi.zmpapi_models").setLevel(logging.INFO)
logging.getLogger("zmp_openapi_toolkit.toolkits.toolkit").setLevel(logging.INFO)

if __name__ == "__main__":
    mixed_api_spec_config = MixedAPISpecConfig.from_mixed_spec_file(
        file_path="samples/openapi/zmp_mixed_api_spec.json"
    )

    zmp_api_wrapper = ZmpAPIWrapper(
        "https://your.server.com", mixed_api_spec_config=mixed_api_spec_config
    )
    toolkit = ZmpToolkit.from_zmp_api_wrapper(zmp_api_wrapper=zmp_api_wrapper)
    tools: List[ZmpTool] = toolkit.get_tools()

```

For more detailed usage instructions, please refer to our [documentation](link).

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/zmp-openapi-toolkit.git
cd zmp-openapi-toolkit
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install development dependencies
```bash
poetry install
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Issue Tracker: https://github.com/yourusername/zmp-openapi-toolkit/issues
- Email: kilsoo75@gmail.com


