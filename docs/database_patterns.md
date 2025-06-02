# Database Connection Patterns

This document describes the database connection management patterns used in the AI Client Agent MCP project.

## Core Components

### Database Class

The `Database` class in `backend/core/database.py` implements a singleton pattern for database connection management, ensuring only one connection pool is created per application instance.

Key features:
- Asynchronous connection pool
- Configurable pool size and timeout settings
- Context manager support for automatic connection handling

## Connection Management Decorators

### `@with_db_connection` Decorator

This decorator simplifies database operations by automatically handling connection acquisition and release.

#### Usage

```python
from backend.core.decorators import with_db_connection

@with_db_connection
async def get_client(client_id: int, conn=None):
    """
    Retrieve a client by ID.
    Args:
        client_id: The ID of the client to retrieve
        conn: Optional database connection (will be provided by the decorator if None)
    Returns:
        Client record or None if not found
    """
    return await conn.fetchrow("SELECT * FROM clients WHERE id = $1", client_id)
```

#### How It Works

1. If a connection is provided, it uses that connection
2. If no connection is provided, it acquires a new connection from the pool
3. The connection is automatically released after the function completes
4. Any exceptions are logged and re-raised

#### Benefits

- Reduces boilerplate code
- Ensures connections are properly released
- Provides consistent error handling
- Allows function composition (a function with the decorator can call another with the decorator)

### `@db_transaction` Decorator

This decorator wraps function execution in a database transaction, ensuring that all operations either succeed or fail together.

#### Usage

```python
from backend.core.decorators import db_transaction

@db_transaction
async def transfer_client_data(source_id: int, target_id: int, conn=None):
    """
    Transfer all data from one client to another and delete the source client.
    Args:
        source_id: The ID of the source client
        target_id: The ID of the target client
        conn: Optional database connection (will be provided by the decorator if None)
    Returns:
        True if the transfer was successful
    """
    # Verify both clients exist
    source = await conn.fetchrow("SELECT * FROM clients WHERE id = $1", source_id)
    target = await conn.fetchrow("SELECT * FROM clients WHERE id = $1", target_id)
    if not source or not target:
        return False
    # Update all invoices to point to the target client
    await conn.execute(
        "UPDATE invoices SET client_id = $1 WHERE client_id = $2", 
        target_id, source_id
    )
    # Delete the source client
    await conn.execute("DELETE FROM clients WHERE id = $1", source_id)
    return True
```

#### How It Works

1. If a connection is provided, it starts a transaction on that connection
2. If no connection is provided, it acquires a new connection and starts a transaction
3. If the function completes successfully, the transaction is committed
4. If an exception occurs, the transaction is rolled back
5. The connection is released after the transaction is committed or rolled back

#### Benefits

- Ensures data integrity
- Simplifies transaction management
- Provides consistent error handling
- Automatically rolls back on exceptions

## Best Practices

### When to Use Each Pattern

- Use `@with_db_connection` for:
  - Simple read operations
  - Single write operations
  - Operations that don't require transaction semantics

- Use `@db_transaction` for:
  - Operations that modify multiple database records
  - Operations that need to be atomic
  - Operations where partial completion would leave the database in an inconsistent state

### Function Composition

Functions decorated with these decorators can be composed together:

```python
@with_db_connection
async def get_client_data(client_id: int, conn=None):
    return await conn.fetchrow("SELECT * FROM clients WHERE id = $1", client_id)

@db_transaction
async def update_client_with_validation(client_id: int, new_data: dict, conn=None):
    # This will use the transaction's connection
    current_data = await get_client_data(client_id, conn)
    if not current_data:
        return False
    # Proceed with update
    await conn.execute(
        "UPDATE clients SET name = $1, email = $2 WHERE id = $3",
        new_data.get("name", current_data["name"]),
        new_data.get("email", current_data["email"]),
        client_id
    )
    return True
```

### Connection Passing

When calling functions from within service methods:

1. **Best Practice**: Always pass the connection object to downstream functions
2. **Why**: Reduces connection pool pressure and ensures transaction consistency

```python
@db_transaction
async def complex_operation(data: dict, conn=None):
    # Pass the connection to other functions
    client = await create_client(data["client"], conn=conn)
    invoice = await create_invoice(data["invoice"], client_id=client["id"], conn=conn)
    return {"client": client, "invoice": invoice}
```

## Error Handling

The decorators include standardized error handling:

1. Database errors are logged with appropriate context
2. Connections are properly released even when exceptions occur
3. Transactions are rolled back on any exception

Custom error handling can be added within the decorated functions:

```python
@with_db_connection
async def get_client_safely(client_id: int, conn=None):
    try:
        return await conn.fetchrow("SELECT * FROM clients WHERE id = $1", client_id)
    except Exception as e:
        logger.error(f"Error retrieving client {client_id}: {str(e)}")
        return None
```

## Testing

When writing tests for functions using these decorators:

1. Use the `db_conn` fixture in tests to provide a connection
2. Ensure tests are wrapped in transactions that are rolled back

Example:

```python
async def test_client_creation(db_conn):
    # The db_conn fixture provides a connection in a transaction
    # that will be rolled back after the test
    client_data = {"name": "Test Client", "email": "test@example.com"}
    # Pass the connection explicitly in tests
    result = await create_client(client_data, conn=db_conn)
    assert result["name"] == "Test Client"
    assert result["id"] is not None
``` 