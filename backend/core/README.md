# Core Components

This directory contains core utilities and infrastructure components used throughout the application.

## Database Connection Management

### Database Class

The `database.py` module defines the `Database` class, which implements a singleton pattern for PostgreSQL connection management:

- Creates and manages a connection pool
- Provides connection acquisition and release methods
- Implements an async context manager for simplified connection handling
- Configurable through environment variables

Usage:

```python
from backend.core.database import database

# Using context manager (preferred)
async with database.connection() as conn:
    result = await conn.fetch("SELECT * FROM clients")

# Manual connection management
conn = await database.acquire()
try:
    result = await conn.fetch("SELECT * FROM clients")
finally:
    await database.release(conn)
```

## Decorators

The `decorators.py` module provides function decorators that simplify database operations:

### with_db_connection

This decorator handles connection acquisition and release automatically:

```python
from backend.core.decorators import with_db_connection

@with_db_connection
async def get_data(id: int, conn=None):
    return await conn.fetchrow("SELECT * FROM data WHERE id = $1", id)
```

### db_transaction

This decorator wraps a function in a database transaction, ensuring all operations either succeed or fail together:

```python
from backend.core.decorators import db_transaction

@db_transaction
async def update_related_data(id: int, data: dict, conn=None):
    # All these operations will be in a single transaction
    await conn.execute("UPDATE table1 SET field = $1 WHERE id = $2", data["field1"], id)
    await conn.execute("INSERT INTO table2 (parent_id, value) VALUES ($1, $2)", id, data["field2"])
    return True
```

## Configuration

The `config.py` module provides a centralized location for application configuration:

- Loads environment variables from `.env` files
- Defines default values for required configuration
- Validates configuration at startup

## Logging

The `logging.py` module configures structured logging for the application:

- Sets up formatters and handlers
- Provides a `get_logger` function to obtain a logger with appropriate context
- Configures log levels based on environment

Usage:

```python
from backend.core.logging import get_logger

logger = get_logger(__name__)

logger.info("Operation started", extra={"operation_id": 123})
try:
    # Do something
    logger.debug("Operation details", extra={"details": "some details"})
except Exception as e:
    logger.error("Operation failed", exc_info=e, extra={"operation_id": 123})
```

## Error Handling

The `errors.py` module defines custom exception classes and error handling utilities:

- `DatabaseError`: Base class for database-related errors
- `NotFoundError`: Raised when a requested resource is not found
- `ValidationError`: Raised when input validation fails
- `format_exception`: Helper function to format exceptions for logging

## Best Practices

1. Use the `database` instance from `database.py` instead of creating your own connections
2. Prefer the context manager syntax for connection handling
3. Use decorators to simplify database operations in service functions
4. Always handle database errors appropriately
5. Use structured logging with context for better troubleshooting 