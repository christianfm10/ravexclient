"""
Unit tests for custom exceptions.

Tests cover:
- Exception inheritance
- Exception attributes
- Exception messages
"""

import pytest

from ravexclient.exceptions import (
    RavexClientError,
    HTTPError,
    ProxyError,
    AuthenticationError,
    ConfigurationError,
    TimeoutError,
)


class TestRavexClientError:
    """Tests for base RavexClientError."""

    def test_exception_creation(self):
        """Test basic exception creation."""
        error = RavexClientError("Test error")

        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {}

    def test_exception_with_details(self):
        """Test exception with additional details."""
        error = RavexClientError("Test error", detail1="value1", detail2="value2")

        assert error.message == "Test error"
        assert error.details["detail1"] == "value1"
        assert error.details["detail2"] == "value2"

    def test_exception_is_exception(self):
        """Test that RavexClientError is a proper Exception."""
        error = RavexClientError("Test")

        assert isinstance(error, Exception)


class TestHTTPError:
    """Tests for HTTPError."""

    def test_http_error_creation(self):
        """Test basic HTTP error creation."""
        error = HTTPError("Request failed")

        assert error.message == "Request failed"
        assert error.status_code is None
        assert error.response_body is None

    def test_http_error_with_status_code(self):
        """Test HTTP error with status code."""
        error = HTTPError("Not found", status_code=404)

        assert error.message == "Not found"
        assert error.status_code == 404

    def test_http_error_with_response_body(self):
        """Test HTTP error with response body."""
        response_body = {"error": "Not found", "detail": "User not found"}
        error = HTTPError("Not found", status_code=404, response_body=response_body)

        assert error.message == "Not found"
        assert error.status_code == 404
        assert error.response_body == response_body
        assert error.response_body["error"] == "Not found"  # type: ignore

    def test_http_error_inherits_from_ravex_client_error(self):
        """Test that HTTPError inherits from RavexClientError."""
        error = HTTPError("Test")

        assert isinstance(error, RavexClientError)
        assert isinstance(error, Exception)

    def test_http_error_details(self):
        """Test HTTP error stores details correctly."""
        error = HTTPError(
            "Server error", status_code=500, response_body={"error": "Internal error"}
        )

        assert error.details["status_code"] == 500
        assert error.details["response_body"] == {"error": "Internal error"}


class TestProxyError:
    """Tests for ProxyError."""

    def test_proxy_error_creation(self):
        """Test basic proxy error creation."""
        error = ProxyError("Proxy connection failed")

        assert error.message == "Proxy connection failed"
        assert isinstance(error, RavexClientError)

    def test_proxy_error_with_details(self):
        """Test proxy error with additional details."""
        error = ProxyError(
            "Proxy timeout", proxy_address="proxy.example.com:8080", timeout=30
        )

        assert error.message == "Proxy timeout"
        assert error.details["proxy_address"] == "proxy.example.com:8080"
        assert error.details["timeout"] == 30


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_authentication_error_creation(self):
        """Test basic authentication error creation."""
        error = AuthenticationError("Invalid credentials")

        assert error.message == "Invalid credentials"
        assert isinstance(error, RavexClientError)

    def test_authentication_error_with_details(self):
        """Test authentication error with details."""
        error = AuthenticationError(
            "Token expired", token_type="Bearer", expired_at="2025-12-13T10:00:00Z"
        )

        assert error.message == "Token expired"
        assert error.details["token_type"] == "Bearer"
        assert error.details["expired_at"] == "2025-12-13T10:00:00Z"


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_configuration_error_creation(self):
        """Test basic configuration error creation."""
        error = ConfigurationError("Invalid configuration")

        assert error.message == "Invalid configuration"
        assert isinstance(error, RavexClientError)

    def test_configuration_error_with_details(self):
        """Test configuration error with details."""
        error = ConfigurationError(
            "Invalid proxy format",
            provided_value="invalid-proxy",
            expected_format="host:port",
        )

        assert error.message == "Invalid proxy format"
        assert error.details["provided_value"] == "invalid-proxy"
        assert error.details["expected_format"] == "host:port"


class TestTimeoutError:
    """Tests for TimeoutError."""

    def test_timeout_error_creation(self):
        """Test basic timeout error creation."""
        error = TimeoutError("Request timed out")

        assert error.message == "Request timed out"
        assert isinstance(error, RavexClientError)

    def test_timeout_error_with_details(self):
        """Test timeout error with details."""
        error = TimeoutError(
            "Connection timeout", timeout_seconds=30, endpoint="/api/users"
        )

        assert error.message == "Connection timeout"
        assert error.details["timeout_seconds"] == 30
        assert error.details["endpoint"] == "/api/users"


class TestExceptionHierarchy:
    """Tests for exception hierarchy and inheritance."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all exceptions inherit from RavexClientError."""
        exceptions = [
            HTTPError("test"),
            ProxyError("test"),
            AuthenticationError("test"),
            ConfigurationError("test"),
            TimeoutError("test"),
        ]

        for error in exceptions:
            assert isinstance(error, RavexClientError)
            assert isinstance(error, Exception)

    def test_exceptions_can_be_caught_by_base(self):
        """Test that specific exceptions can be caught by base class."""
        try:
            raise HTTPError("Test error", status_code=404)
        except RavexClientError as e:
            assert e.message == "Test error"
            assert isinstance(e, HTTPError)

    def test_exceptions_can_be_caught_individually(self):
        """Test that exceptions can be caught by their specific type."""
        try:
            raise ProxyError("Proxy failed")
        except ProxyError as e:
            assert e.message == "Proxy failed"
        except RavexClientError:
            pytest.fail("Should have been caught by ProxyError")
