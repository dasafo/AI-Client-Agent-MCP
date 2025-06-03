# Data Models

This directory contains Pydantic models that define the data structures and validation rules for the application.

## Model Definitions

### Client Models (`client.py`)
- `ClientCreate`: Schema for creating new clients
- `ClientUpdate`: Schema for updating existing clients
- `ClientOut`: Schema for client data returned by the API

### Invoice Models (`invoice.py`)
- `InvoiceCreate`: Schema for creating new invoices
- `InvoiceUpdate`: Schema for updating existing invoices
- `InvoiceOut`: Schema for invoice data returned by the API

### Report Models (`report.py`)
- `ReportOut`: Schema for report data stored in the database

## Usage Example

```python
from backend.models.client import ClientCreate

# Create a new client
client_data = ClientCreate(
    name="John Doe",
    city="New York",
    email="john@example.com"
)

# The model will validate the data
# Invalid data will raise ValidationError
```

## Features

- Automatic data validation
- Type checking
- JSON serialization/deserialization
- Clear error messages for invalid data
- Documentation through type hints

## Best Practices

1. Use models for all data validation
2. Keep models focused and single-purpose
3. Document model fields with descriptive comments
4. Use appropriate field types and validators
5. Consider adding custom validators for complex rules 