# Testing Guide

This directory contains test suites for the AI Client Agent MCP project.

## Test Structure

The tests are organized into the following directories:

- `integration/`: Tests that verify the interaction between components
- `unit/`: Tests for individual functions and classes

## Test Configuration

The `conftest.py` file contains pytest fixtures used across the test suite:

- `db_engine_pool`: Creates a connection pool for testing
- `db_conn`: Provides a database connection within a transaction
- Custom fixtures for testing specific components

## Environment Variables

Tests use environment variables from `tests/.env.test` to configure the test database. Key variables:

- `DB_USER_TEST`: Database user for tests (defaults to main DB_USER if not set)
- `DB_PASSWORD_TEST`: Database password for tests (defaults to main DB_PASSWORD if not set)
- `DB_HOST_TEST`: Database host for tests (default: localhost)
- `DB_PORT_TEST`: Database port for tests (default: 5433)
- `DB_NAME_TEST`: Database name for tests (default: ai_client_mcp_db_for_tests)

## Running Tests

Run the entire test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/integration/test_client_services.py
```

Run a specific test function:

```bash
pytest tests/integration/test_client_services.py::test_create_and_get_client
```

## Test Database

The test fixtures will:

1. Create a test database if it doesn't exist
2. Create all necessary tables for testing
3. Execute each test in a transaction that is rolled back after the test completes

This ensures tests don't interfere with each other and the database is left in a clean state.

## Writing Tests

### Basic Test Structure

```python
# Import the fixture to get a database connection
import pytest
from backend.services import client_service

# Use the db_conn fixture to get a database connection
async def test_create_client(db_conn):
    # Test data
    client_data = {
        "name": "Test Client",
        "email": "test@example.com",
        "city": "Test City"
    }
    
    # Call the service function with the test connection
    result = await client_service.create_client(client_data, conn=db_conn)
    
    # Assert the expected results
    assert result["name"] == client_data["name"]
    assert result["email"] == client_data["email"]
    assert result["city"] == client_data["city"]
    assert "id" in result
```

### Test Isolation

Each test using the `db_conn` fixture runs in its own transaction, which is rolled back after the test completes. This ensures test isolation without requiring database cleanup.

### Testing Services with Decorators

When testing service functions that use the `@with_db_connection` or `@db_transaction` decorators:

```python
async def test_service_with_decorator(db_conn):
    # The db_conn fixture provides a connection in a transaction
    
    # Always pass the connection explicitly in tests
    result = await service_function(params, conn=db_conn)
    
    # Assert expected results
    assert result == expected_value
```

### Testing Transactions

For testing functions that use transactions:

```python
async def test_transaction_function(db_conn):
    # Setup initial data
    client1 = await client_service.create_client({"name": "Client 1"}, conn=db_conn)
    client2 = await client_service.create_client({"name": "Client 2"}, conn=db_conn)
    
    # Test the transaction function
    result = await client_service.transfer_client_data(
        source_id=client1["id"], 
        target_id=client2["id"],
        conn=db_conn
    )
    
    # Verify the transaction results
    assert result is True
    
    # Verify source client no longer exists
    source_client = await client_service.get_client_by_id(client1["id"], conn=db_conn)
    assert source_client is None
    
    # Verify target client still exists
    target_client = await client_service.get_client_by_id(client2["id"], conn=db_conn)
    assert target_client is not None
```

## Best Practices

1. Always use the `db_conn` fixture for database tests
2. Make each test independent and not rely on data created by other tests
3. Use descriptive test names that indicate what is being tested
4. Test both successful operations and error cases
5. Mock external dependencies when appropriate
6. Keep tests focused on a single functionality 