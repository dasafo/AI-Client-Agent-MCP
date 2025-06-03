# MCP Tools

This directory contains the FastMCP tool definitions that expose the application's functionality to AI agents and automated systems.

## Tool Categories

### Client Tools (`client_tools.py`)
- `list_clients`: Lists all clients in the database
- `get_client`: Retrieves a specific client by ID
- `create_client`: Creates a new client
- `update_client`: Updates an existing client
- `delete_client`: Deletes a client

### Invoice Tools (`invoice_tools.py`)
- `list_invoices`: Lists all invoices
- `get_invoice`: Retrieves a specific invoice by ID
- `list_client_invoices`: Lists all invoices for a specific client
- `create_invoice`: Creates a new invoice
- `update_invoice`: Updates an existing invoice
- `delete_invoice`: Deletes an invoice

### Report Tools (`report_tools.py`)
- `generate_report`: Generates and sends professional business reports to authorized managers
  - Requires valid API token
  - Validates manager authorization
  - Generates HTML report with charts
  - Sends report via email
  - Stores report in database

## Usage Example

```python
# Using an MCP client
response = generate_report(
    client_name="John Doe",
    period="2024",
    manager_name="David Salas",
    manager_email="dsf@protonmail.com",
    report_type="detailed",
    api_token="your-api-token"
)
```

## Security

- All tools validate input data using Pydantic models
- Report generation requires API token authentication
- Manager authorization is verified before sending reports
- HTML content is sanitized to prevent XSS attacks

## Best Practices

1. Always validate input parameters
2. Handle errors gracefully and provide meaningful messages
3. Use appropriate logging for debugging
4. Follow the established naming conventions
5. Document new tools thoroughly 