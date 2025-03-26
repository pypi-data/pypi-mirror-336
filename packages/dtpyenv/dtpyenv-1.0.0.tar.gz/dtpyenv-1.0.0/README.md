# Environment Manager

A Python class for managing environment variables in an organized and controlled manner. This package provides an easy-to-use interface to load environment variables from a file, register allowed variables, and access them statically, with support for case-insensitivity and caching.

## Features

- **Load environment variables** from a `.env` file.
- **Override existing variables** with the option to allow or deny.
- **Register allowed variables** to control which variables can be accessed.
- **Case-insensitive access** to environment variables.
- **Caching** for efficient future access to environment variables.
- **Logging** for missing files or unregistered variables.

## Installation

To install this package, run the following command:

```bash
pip install dtpyenv
```

