# Advanced Logs

`dtpylog` is a lightweight Python package designed to provide an advanced logging system. It allows you to log messages and events both locally and remotely using a configurable API. You can log messages in different levels (info, debug, warning, error) and have them stored or printed depending on your configuration.

## Features

- **Remote Logging**: Send logs to a remote logging service via an API with retries and exponential backoff.
- **Custom Handlers**: Supports console logging and file-based logging using rotating file handlers.
- **Flexible Configuration**: Easily configure logging behavior (e.g., log levels, API keys, etc.) via a Singleton `Config` class.
- **Celery Mode Support**: Special logging configuration for Celery tasks.
- **Custom Formatting**: Custom log message formatting with support for additional details in the logs.

## Installation

You can install the package directly with pip.

```bash
pip install dtpylog
```
