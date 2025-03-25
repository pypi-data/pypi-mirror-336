# Jupyter Server Favicon Extension

[![PyPI version](https://badge.fury.io/py/jupyter-server-favicon.svg)](https://badge.fury.io/py/jupyter-server-favicon)
[![Python Versions](https://img.shields.io/pypi/pyversions/jupyter-server-favicon.svg)](https://pypi.org/project/jupyter-server-favicon/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Sponsored by [Enverge.ai](https://enverge.ai)** - Simpler, greener, cheaper AI training platform. Enverge harnesses excess green energy for powerful, cost-effective computing on GPUs, enabling environmentally friendly AI model development, training, and fine-tuning. Currently in private alpha with limited spots available.

A Jupyter Server extension that adds favicon support to your Jupyter Server instance, making it easier to identify your Jupyter tabs in the browser.

![demo](./enverge-favicon.gif)

## Features

- Automatically serves a favicon for your Jupyter Server instance
- Easy to install and configure
- Compatible with all modern browsers
- No additional configuration required

## Installation

You can install the extension using pip:

```bash
pip install jupyter-server-favicon
```

Or if you want to install from source:

```bash
# Clone the repository
git clone https://github.com/Enverge-Labs/jupyter-server-favicon.git
cd jupyter-server-favicon

# Create a conda environment (optional but recommended)
conda create -y -n jupyter-server-favicon python=3.9
conda activate jupyter-server-favicon

# Install in development mode
pip install -e .
```

## Usage

The extension is automatically enabled after installation. Simply start Jupyter Server:

```bash
jupyter server
```

The favicon will be automatically served at `/static/jupyter_server_favicon/favicon.ico`.

## Development

To set up the development environment:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy .
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub repository](https://github.com/Enverge-Labs/jupyter-server-favicon/issues).
