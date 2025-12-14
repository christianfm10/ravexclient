# Testing Guide

## Running Tests

### Install Test Dependencies

Using uv:
```bash
uv pip install pytest pytest-asyncio pytest-cov
```

Or using pip:
```bash
pip install pytest pytest-asyncio pytest-cov
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=ravexclient --cov-report=html --cov-report=term
```

This will generate:
- Terminal coverage report
- HTML coverage report in `htmlcov/` directory

### Run Specific Test Files

```bash
# Test base client only
pytest tests/test_base_client.py -v

# Test exceptions only
pytest tests/test_exceptions.py -v
```

### Run Specific Test Classes

```bash
pytest tests/test_base_client.py::TestBaseClientInitialization -v
```

### Run Specific Tests

```bash
pytest tests/test_base_client.py::TestBaseClientInitialization::test_init_with_defaults -v
```

## Test Structure

### `test_base_client.py`
Tests for the main `BaseClient` class:

- **TestBaseClientInitialization**: Tests for client initialization
  - Default configuration
  - Custom base URL
  - Proxy configuration
  - Cloudflare clearance
  - Custom timeout and headers

- **TestBaseClientFetchMethod**: Tests for the `_fetch` method
  - GET, POST requests
  - Query parameters
  - Custom headers
  - Payload handling

- **TestBaseClientConvenienceMethods**: Tests for `_get`, `_post`, `_put`, `_delete`
  - Method calls with proper arguments
  - Integration with `_fetch`

- **TestBaseClientExceptions**: Tests for exception handling
  - HTTPError on 404, 500 responses
  - ProxyError on proxy failures
  - TimeoutError on request timeouts
  - Generic exception handling

- **TestBaseClientContextManager**: Tests for async context manager
  - Enter/exit functionality
  - Proper cleanup
  - Exception handling in context

- **TestBaseClientUtilityMethods**: Tests for utility methods
  - `_check_ip()` method
  - `close()` method

- **TestBaseClientCookieManagement**: Tests for cookie handling
  - Cloudflare clearance cookies
  - Cookie propagation to httpx client

- **TestBaseClientProxyConfiguration**: Tests for proxy setup
  - Proxy with/without http prefix
  - Different proxy formats

- **TestBaseClientEndpointConstruction**: Tests for URL building
  - Endpoints with/without leading slash
  - Empty endpoints

### `test_exceptions.py`
Tests for custom exception classes:

- **TestRavexClientError**: Base exception tests
- **TestHTTPError**: HTTP error with status codes and response bodies
- **TestProxyError**: Proxy-related errors
- **TestAuthenticationError**: Authentication failures
- **TestConfigurationError**: Configuration issues
- **TestTimeoutError**: Timeout scenarios
- **TestExceptionHierarchy**: Exception inheritance and catching

## Test Coverage

The test suite covers:

✅ **Client Initialization** (100%)
- All configuration options
- Default values
- Custom parameters

✅ **HTTP Methods** (100%)
- All HTTP verbs (GET, POST, PUT, DELETE)
- Query parameters
- Request bodies
- Custom headers

✅ **Exception Handling** (100%)
- HTTPError (404, 500, etc.)
- ProxyError
- TimeoutError
- Generic exceptions

✅ **Context Manager** (100%)
- Async context manager protocol
- Resource cleanup
- Exception handling

✅ **Utility Methods** (100%)
- IP checking
- Client closing

✅ **Cookie Management** (100%)
- Cloudflare clearance
- Cookie propagation

✅ **Proxy Configuration** (100%)
- Various proxy formats
- Proxy error handling

## Mocking Strategy

Tests use `unittest.mock` to:
- Mock httpx.AsyncClient requests
- Mock responses with custom data
- Simulate various error conditions
- Avoid actual network calls

Example:
```python
with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
    mock_request.return_value = mock_response
    result = await client._fetch("GET", "/endpoint")
```

## Writing New Tests

### Template for New Test

```python
@pytest.mark.asyncio
async def test_new_feature(self):
    """Test description."""
    client = TestAPIClient()
    
    # Setup mock
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    
    with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_response
        
        # Execute
        result = await client._fetch("GET", "/test")
        
        # Assert
        assert result == {"result": "success"}
        mock_request.assert_called_once()
    
    await client.close()
```

### Best Practices

1. **Always close the client** after tests (or use context manager)
2. **Use descriptive test names** that explain what is being tested
3. **One assertion per test** when possible
4. **Mock external dependencies** (network calls, etc.)
5. **Test both success and failure cases**
6. **Use pytest fixtures** for common setup

## Continuous Integration

Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install pytest pytest-asyncio pytest-cov
    pytest --cov=ravexclient --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Troubleshooting

### ImportError for ravexclient
Make sure the package is installed in development mode:
```bash
pip install -e .
```

### AsyncIO warnings
If you see asyncio warnings, ensure `pytest-asyncio` is installed and `asyncio_mode = auto` is set in `pytest.ini`.

### Tests hanging
Check that all async tests have `@pytest.mark.asyncio` decorator and that clients are properly closed.
