# AI Client Agent MCP

## Project Overview

The AI Client Agent MCP (Master Control Program) is a backend application designed to manage clients and their associated invoices. It provides a set of tools (API endpoints) that can be invoked by an AI agent or other systems to perform CRUD (Create, Read, Update, Delete) operations on client and invoice data.

The project is built with Python, utilizing FastAPI for the web server, Pydantic for data validation and serialization, and `asyncpg` for asynchronous interaction with a PostgreSQL database. The tools are exposed via an MCP interface, allowing for programmatic interaction.

## Core Features

*   **Client Management**:
    *   Create new clients (name, city, email).
    *   Retrieve a list of all clients.
    *   Get details for a specific client by ID.
    *   Update existing client information.
    *   Delete clients.
*   **Invoice Management**:
    *   Create new invoices for clients (amount, issue date, due date, status).
    *   List all invoices.
    *   Get details for a specific invoice by ID.
    *   List all invoices for a specific client.
    *   Update existing invoice information.
    *   Delete invoices.
*   **Asynchronous Operations**: Leverages Python's `asyncio` and `asyncpg` for non-blocking database operations, suitable for high-concurrency environments.
*   **Data Validation**: Uses Pydantic models to ensure data integrity and provide clear validation errors.
*   **MCP Tooling**: Exposes business logic through an MCP agent interface, enabling integration with AI agents or other automated systems.

## Project Structure

```
.
├── .env                # Environment variables (database connection, etc.)
├── .venv/              # Python virtual environment
├── backend/
│   ├── __init__.py
│   ├── server.py         # Main FastAPI application and MCP server runner
│   ├── mcp_instance.py   # MCP agent instance
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── tools/      # MCP tool definitions
│   │           ├── __init__.py
│   │           ├── client_tools.py
│   │           └── invoice_tools.py
│   ├── models/           # Pydantic models for data validation & serialization
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── invoice.py
│   └── services/         # Business logic and database interaction
│       ├── __init__.py
│       ├── client_service.py
│       └── invoice_service.py
├── database/
│   ├── __init__.py
│   └── create_tables.sql # SQL script to create database tables
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── tests/                # (Placeholder for tests)
```

## Setup and Installation

### Prerequisites

*   Python 3.8+
*   PostgreSQL database server

### 1. Clone the Repository (if applicable)

```bash
git clone <repository_url>
cd AI-Client-Agent-MCP
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the `.env.example` (if one exists, otherwise create `.env`) and fill in your database connection details:

```env
# .env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_client_mcp_db
```

### 5. Setup Database

Ensure your PostgreSQL server is running. Connect to your PostgreSQL instance and create the database specified in `.env` (e.g., `ai_client_mcp_db`).

Then, run the `create_tables.sql` script to set up the necessary tables. You can use a tool like `psql`:

```bash
psql -U your_db_user -d ai_client_mcp_db -a -f database/create_tables.sql
```
(You might need to enter your password)

## Running the Application

To start the backend server and MCP agent:

```bash
python -m backend.server
```

The server will start, and the MCP agent will register its tools. You should see log output indicating that the server is running and tools are available. Check `startup_env.log` for basic startup information.

## API Tools (via MCP Agent)

The application exposes its functionality through MCP tools. An MCP client can connect to the server and invoke these tools.

**Client Tools:**
*   `list_clients`: Lists all clients.
*   `get_client(client_id: int)`: Retrieves a specific client.
*   `create_client(name: str, city: Optional[str], email: Optional[str])`: Creates a new client.
*   `update_client(client_id: int, name: Optional[str], city: Optional[str], email: Optional[str])`: Updates a client.
*   `delete_client(client_id: int)`: Deletes a client.

**Invoice Tools:**
*   `list_invoices`: Lists all invoices.
*   `get_invoice(invoice_id: int)`: Retrieves a specific invoice.
*   `list_client_invoices(client_id: int)`: Lists all invoices for a specific client.
*   `create_invoice(client_id: int, amount: str, issued_at: Optional[str], due_date: Optional[str], status: Optional[str])`: Creates an invoice.
*   `update_invoice(invoice_id: int, client_id: Optional[str], amount: Optional[str], issued_at: Optional[str], due_date: Optional[str], status: Optional[str])`: Updates an invoice.
*   `delete_invoice(invoice_id: int)`: Deletes an invoice.

*Note: For string date fields (`issued_at`, `due_date`), use ISO format (YYYY-MM-DD).*

## Development

(Placeholder for development guidelines, running tests, linters, etc.)

## Contributing

(Placeholder for contribution guidelines)

## License

(Placeholder for license information - e.g., MIT, Apache 2.0)