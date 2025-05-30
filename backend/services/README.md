# Services

This directory contains service modules that implement the business logic of the application.

## Available Services

### Client Service

The `client_service.py` module provides functions for managing clients in the database.

Key functions:
- `get_all_clients`: Retrieve all clients
- `get_client_by_id`: Get a specific client by ID
- `create_client`: Create a new client
- `update_client`: Update an existing client
- `delete_client`: Delete a client by ID
- `transfer_client_data`: Transfer data from one client to another (transactional)

### Invoice Service

The `invoice_service.py` module provides functions for managing invoices in the database.

Key functions:
- `get_all_invoices`: Retrieve all invoices
- `get_invoice_by_id`: Get a specific invoice by ID
- `get_invoices_by_client_id`: Get all invoices for a specific client
- `create_invoice`: Create a new invoice
- `update_invoice`: Update an existing invoice
- `delete_invoice`: Delete an invoice by ID
- `create_invoice_with_verification`: Create an invoice with client verification (transactional)

## Usage Patterns

All service functions follow a consistent pattern:

1. They are decorated with `@with_db_connection` or `@db_transaction` from `backend.core.decorators`
2. They accept an optional `conn` parameter which, if provided, will be used instead of creating a new connection
3. They return structured data or raise exceptions with clear error messages

### Basic Usage

```python
from backend.services import client_service, invoice_service

# Get all clients
clients = await client_service.get_all_clients()

# Create a client
new_client = await client_service.create_client({
    "name": "New Client", 
    "email": "client@example.com",
    "city": "New York"
})

# Get invoices for a client
client_invoices = await invoice_service.get_invoices_by_client_id(new_client["id"])
```

### Connection Reuse

To improve performance when making multiple database calls, you can reuse a connection:

```python
from backend.core.database import database

async with database.connection() as conn:
    # Use the same connection for multiple operations
    client = await client_service.get_client_by_id(1, conn=conn)
    invoices = await invoice_service.get_invoices_by_client_id(1, conn=conn)
```

### Transactional Operations

For operations that need to be atomic, use the transaction-specific functions:

```python
# Transfer all data from one client to another in a transaction
success = await client_service.transfer_client_data(source_id=1, target_id=2)

# Create an invoice with client verification in a transaction
invoice = await invoice_service.create_invoice_with_verification(
    client_id=1, 
    amount="100.00", 
    status="pending"
)
```

## Error Handling

Service functions handle database errors and raise appropriate exceptions:

```python
try:
    client = await client_service.get_client_by_id(999)
    if client is None:
        # Handle not found case
        print("Client not found")
except Exception as e:
    # Handle database errors
    print(f"Database error: {str(e)}")
```

## Integration with MCP

These services are integrated with the MCP system through tools defined in:
- `backend/api/client_tools.py`
- `backend/api/invoice_tools.py`

The tools handle parameter validation and conversion between MCP's data format and the service functions.

## Best Practices

1. Always use the service functions instead of direct database queries
2. Pass connections when making multiple related queries
3. Use transactional methods for operations that modify multiple records
4. Handle the case where functions return `None` for not found items 