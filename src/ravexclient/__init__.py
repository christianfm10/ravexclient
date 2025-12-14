"""
RavexClient - Base HTTP client for building API clients.

This package provides a flexible and extensible base class for creating
async HTTP clients with built-in support for proxies, authentication,
and error handling.
"""

from .base import BaseClient
from .exceptions import (
    RavexClientError,
    HTTPError,
    ProxyError,
    AuthenticationError,
    ConfigurationError,
    TimeoutError,
)

__version__ = "0.1.0"
__all__ = [
    "BaseClient",
    "RavexClientError",
    "HTTPError",
    "ProxyError",
    "AuthenticationError",
    "ConfigurationError",
    "TimeoutError",
]


def main() -> None:
    """Entry point for CLI if needed."""
    print("RavexClient v" + __version__)
    print("Base HTTP client library for building API clients.")
    print("\nFor usage examples, see: https://github.com/your-repo/ravexclient")
