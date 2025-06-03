# Integration Tests

This directory contains integration tests that verify the interaction between different components of the application.

## Test Files

### `test_client_services.py`
- Tests client service integration with database
- Verifies CRUD operations
- Tests transaction handling
- Validates error scenarios

### `test_invoice_services.py`
- Tests invoice service integration with database
- Verifies invoice-client relationships
- Tests status transitions
- Validates business rules

## Test Database

Tests use a dedicated test database that is:
- Created before tests run
- Reset between test cases
- Dropped after all tests complete

## Example Test

```python
import pytest
from backend.services import client_service

@pytest.mark.asyncio
async def test_create_and_get_client(db_conn):
    # Create a client
    client = await client_service.create_client(
        name="Test Client",
        city="Test City",
        email="test@example.com",
        conn=db_conn
    )
    
    # Verify creation
    assert client["name"] == "Test Client"
    
    # Retrieve and verify
    retrieved = await client_service.get_client_by_id(
        client_id=client["id"],
        conn=db_conn
    )
    assert retrieved["email"] == "test@example.com"
```

## Test Isolation

Each test:
- Runs in its own transaction
- Has a clean database state
- Doesn't affect other tests
- Cleans up after itself

## Best Practices

1. Use the `db_conn` fixture for database access
2. Test complete workflows
3. Verify data integrity
4. Test error conditions
5. Keep tests independent
6. Use descriptive test names 