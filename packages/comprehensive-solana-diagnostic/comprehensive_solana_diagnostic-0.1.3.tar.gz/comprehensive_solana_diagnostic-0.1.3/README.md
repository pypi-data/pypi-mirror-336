[![PyPI version](https://badge.fury.io/py/comprehensive-solana-diagnostic.svg)](https://pypi.org/project/comprehensive-solana-diagnostic/)

# Comprehensive Solana Diagnostic Tool

A Python tool for comprehensive diagnostics of Solana nodes and networks.

## Installation

```bash
pip install comprehensive-solana-diagnostic
```

## Usage

```bash
solana-diagnostic [options]
```

## Features

- Network status monitoring
- Validator performance analysis
- RPC endpoint health checks
- Detailed error reporting

## Project Structure

```
comprehensive_solana_diagnostic/
├── comprehensive_solana_diagnostic/
│   ├── __init__.py
│   ├── comprehensive_solana_diagnostic.py
│   └── network_handler.py
├── tests/
│   ├── __init__.py
│   ├── test_network_handler.py
│   └── test_main.py
├── setup.py
├── README.md
├── CHANGELOG.md
└── requirements.txt
```

This shows the main project structure with the core implementation, tests, and configuration files.

## Example Output

```bash
$ solana-diagnostic
🔍 Comprehensive Solana Library Diagnostic
==================================================

📋 Python Environment:
Version: 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0]
Executable: /path/to/python
Path: [...]

🔬 Solana Library Inspection:
Solana Library Details: {...}

🌐 Solana RPC Connection Test: {...}

📦 Dependency Information: {...}

🔧 Solana-Specific Diagnostics: {...}

✅ Diagnostic Complete
```

This shows the comprehensive diagnostic output the tool provides.

## Running Tests

Install test dependencies:

```bash
pip install -e .[test]
```

Run tests with coverage:

```bash
pytest
```

View coverage report:

```bash
pytest --cov-report html
```

## License

MIT
