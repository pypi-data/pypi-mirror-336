# req-generator

A Python CLI tool that automatically generates requirements.txt by scanning your project for imports.

## Features

- Scans all Python files in your project directory and subdirectories
- Identifies third-party imports (ignores standard library)
- Fetches the latest package versions from PyPI
- Generates a requirements.txt file with exact versions

## Installation

```bash
pip install req-generator