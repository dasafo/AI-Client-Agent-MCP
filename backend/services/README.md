# Business Services

This directory contains the business logic and database interaction services for the application.

## Service Modules

### Client Service (`client_service.py`)
- CRUD operations for clients
- Client data validation
- Database transaction management
- Error handling for client operations

### Invoice Service (`invoice_service.py`)
- CRUD operations for invoices
- Invoice status management
- Client-invoice relationship handling
- Invoice data validation

### Report Service (`report_service.py`)
- Report generation logic
- Manager authorization
- Email sending functionality
- Report storage and retrieval

## Architecture

Services follow these principles:
- Dependency injection for database connections
- Transaction management
- Error handling and logging
- Clear separation of concerns

## Usage Example

```python
from backend.services import client_service

# Create a new client
client = await client_service.create_client(
    name="John Doe",
    city="New York",
    email="john@example.com",
    conn=db_connection
)

# Get client by ID
client_data = await client_service.get_client_by_id(
    client_id=1,
    conn=db_connection
)
```

## Best Practices

1. Use dependency injection for database connections
2. Handle all database errors appropriately
3. Use transactions for multi-step operations
4. Log important operations and errors
5. Keep business logic separate from data access
6. Write comprehensive tests for all services 