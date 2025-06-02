# 🗂️ AI Client Agent MCP

<div align="center">
  <img src="https://img.shields.io/badge/FastMCP-Python-009688?style=for-the-badge&logo=python" alt="FastMCP">
  <img src="https://img.shields.io/badge/PostgreSQL-15--alpine-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL 15-alpine">
  <img src="https://img.shields.io/badge/pgAdmin_4-latest-2496ED?style=for-the-badge&logo=pgadmin" alt="pgAdmin 4">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python" alt="Python 3.11">
</div>

<br>

> **AI Client Agent MCP** is an advanced backend system for managing clients and their invoices (or quotes), designed to be operated by an AI Agent or programmatically. 🚀

🔗 **Relational Database Management:** Built on PostgreSQL, this system works with multiple related tables (clients, invoices, managers, reports, etc.), enabling efficient and secure handling of business data.

📊 **Automated, Professional Reporting:** The agent can query, analyze, and cross-reference data across entities, generating detailed, visually appealing business reports. These reports can be automatically sent via email to authorized managers, streamlining decision-making and business communication.

⚡ **Fully Containerized:** Thanks to Docker, setup and deployment are fast and hassle-free, ensuring portability and scalability.

Perfect for organizations seeking to automate client management, invoicing, and reporting—integrating artificial intelligence and modern workflows into their daily operations.

## 📚 Documentation

- [Quick Start Guide](docs/quickstart.md): Step-by-step setup and development instructions
- [Database Patterns](docs/database_patterns.md): Database connection and transaction management
- [Full Documentation Index](docs/index.md): All docs, guides, and references

## 🔧 Architecture Overview

Below is a simple architecture diagram illustrating the main components and their interactions:

```
+-------------------+         +-------------------+         +-------------------+
| Conversational AI | <-----> | FastMCP (API/Tool)| <-----> | PostgreSQL DB     |
| Agent / Client    |  HTTP   | Backend (FastMCP) |  async  | (asyncpg)         |
+-------------------+         +-------------------+         +-------------------+
```

Or as a Markdown image:

![Architecture Diagram](https://github.com/dasafo/AI-Client-Agent-MCP/blob/main/img/flux.png)

- **Conversational AI Agent**: Can be an agent, script, or user using an MCP client (e.g., Cursor IDE).
- **FastMCP Backend**: Exposes tools (endpoints) for client and invoice management.
- **PostgreSQL DB**: Stores all data, accessed asynchronously.

## 🎯 Core Features

*   👤 **Comprehensive Client Management**: CRUD (Create, Read, Update, Delete) operations for client profiles.
*   📄 **Invoice/Quote Administration**: Full CRUD operations for invoices, linked to clients, including status management (`pending`, `completed`, `canceled`).
*   🚀 **Asynchronous Performance**: Leverages `asyncio` and `asyncpg` for efficient, non-blocking database operations.
*   🛡️ **Rigorous Data Validation**: Employs Pydantic models to ensure data integrity across all interactions.
*   🤖 **MCP Tool Interface**: Exposes business logic through a set of tools for the Master Control Program (FastMCP), facilitating integration with AI agents and automated systems.
*   🐳 **Complete Dockerized Environment**: Includes the application, PostgreSQL database, and pgAdmin 4, all managed with Docker Compose for consistent and straightforward setup and execution.
*   ⚙️ **Flexible Configuration**: Environment variables for easy adaptation to different database setups and ports.
*   🧪 **Extensive Test Coverage**: Comprehensive test suite with database isolation and proper connection management.
*   💉 **Dependency Injection**: Services designed with dependency injection patterns to facilitate testing and flexibility.
*   🧠 **Built-in AI Development**: Adding a `.cursor` directory enables AI-assisted coding directly within the project.

## 🚀 Quick Start (with Docker)

This is the recommended way to set up and run the project.

### Prerequisites
*   [Docker](https://www.docker.com/get-started) installed.
*   Docker Compose (usually included with Docker Desktop; for Linux, install the `docker-compose-plugin`).

### Installation

```bash
# 1. Clone the repository (if you haven't already)
git clone <repository_url>
cd AI-Client-Agent-MCP

# 2. Configure environment variables
cp env.example .env 
# Edit .env with your configurations (see example below)
nano .env #(or your preferred editor)

# 3. Start all services
docker compose up --build
```

### Essential Environment Variables (`.env`)

Your `.env` file should contain at least the following:

```env
# PostgreSQL Database Configuration
DB_USER=db_user
DB_PASSWORD=db_password
DB_NAME=AI-Agent-ddbb
DB_PORT=5432 # Internal port for PostgreSQL in its container

# Application Server Configuration
SERVER_PORT=8000 # Port on localhost to access the MCP server

# pgAdmin 4 Configuration
PGADMIN_EMAIL=admin@example.com # Email for pgAdmin web interface login
PGADMIN_PASSWORD=admin          # Password for pgAdmin login
PGADMIN_PORT=5050         # Port on localhost to access pgAdmin
```
*Note: `DB_HOST` and `SERVER_HOST` are managed by Docker Compose for inter-container communication and host exposure.* 

### Accessing Services

*   **MCP Server (AI Client Agent MCP)**: Connect via an MCP client (e.g., Cursor IDE) to the agent, which internally uses the services. The `server.py` runs on `http://localhost:${SERVER_PORT}` but is primarily for FastMCP's internal communication, not direct HTTP REST access.
*   **pgAdmin 4**: `http://localhost:${PGADMIN_PORT}` (e.g., `http://localhost:5050`)
    *   **pgAdmin Login**: Use `PGADMIN_EMAIL` and `PGADMIN_PASSWORD`.
    *   **Connect to Project DB from pgAdmin**:
        *   Host: `db` (Docker service name)
        *   Port: `5432` (PostgreSQL's internal port)
        *   Database: Your `DB_NAME`
        *   Username: Your `DB_USER`
        *   Password: Your `DB_PASSWORD`

### Useful Docker Compose Commands

```bash
# Start services (and build if necessary)
docker compose up --build
# Stop services
docker compose down
# View real-time logs from services
docker compose logs -f
# Check container status
docker compose ps
# Access a container's shell (e.g., the app)
docker compose exec app /bin/sh
# Access psql in the DB container
docker compose exec db psql -U ${DB_USER} -d ${DB_NAME}
```

## ⚙️ Local Development (Non-Docker Alternative)

For development or specific debugging scenarios outside Docker:

### Prerequisites
*   Python 3.11 (or the version in `Dockerfile`).
*   Locally accessible PostgreSQL server.

### Steps
1.  **Virtual Environment & Dependencies**: `python -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`.
2.  **Configure `.env`**: Ensure `DB_HOST` and `DB_PORT` point to your local PostgreSQL instance.
3.  **Manual Database Setup**: Create the database (`DB_NAME`) and run `psql -U ${DB_USER} -d ${DB_NAME} -a -f database/create_tables.sql`. Also run `psql -U ${DB_USER} -d ${DB_NAME} -a -f database/managers.sql` if you intend to use the reporting tool.
4.  **Run Application**: `python -m backend.server`.

## 🛠️ MCP Tools

The application exposes its functionality through FastMCP tools. An MCP client (like Cursor IDE or a custom script using the `fastmcp` library) can connect to the server and invoke them.

### Client Tools
*   `list_clients`: Lists all clients.
*   `get_client(client_id: int)`: Retrieves a specific client.
*   `create_client(name: str, city: Optional[str], email: Optional[str])`: Creates a new client.
*   `update_client(client_id: int, name: Optional[str], city: Optional[str], email: Optional[str])`: Updates a client.
*   `delete_client(client_id: int)`: Deletes a client.

### Invoice Tools
*   `list_invoices`: Lists all invoices.
*   `get_invoice(invoice_id: int)`: Retrieves a specific invoice.
*   `list_client_invoices(client_id: int)`: Lists all invoices for a specific client.
*   `create_invoice(client_id: int, amount: str, issued_at: Optional[str], due_date: Optional[str], status: Optional[str])`: Creates an invoice. (Valid statuses: `pending`, `completed`, `canceled`)
*   `update_invoice(invoice_id: int, client_id: Optional[str], amount: Optional[str], issued_at: Optional[str], due_date: Optional[str], status: Optional[str])`: Updates an invoice.
*   `delete_invoice(invoice_id: int)`: Deletes an invoice.

*Note: For date fields (`issued_at`, `due_date`), use ISO format (YYYY-MM-DD).* 

## 💡 Use Cases / Application Ideas

The `AI Client Agent MCP` can serve as a foundation for various automated systems:

*   **AI-Powered CRM**: An AI agent could use the FastMCP tools to create and update clients based on email or chat interactions and draft invoices.
*   **Customer Support with Account Management**: Integrate with a ticketing system where an AI agent can query client information and recent invoices for more contextualized responses using FastMCP tools.
*   **Semi-Automated Billing Tool**: A simple interface (or bot) allowing non-technical users to request invoice creation for existing clients, with an AI agent validating or completing data via FastMCP tools.
*   **AI-Assisted Data Migration**: Use an agent to read data from a legacy system and utilize the `create_client` and `create_invoice` FastMCP tools to populate this new system.

## 💬 Conversational Agent Example

Here is an example of how a user or AI agent can interact with the system using natural language or structured tool calls:

### Natural Language Request

> "Give me a detailed report of all completed quotes for client Carolina Padilla and send it to David Salas."

### Structured Tool Call (Python)

```python
# Using an MCP client or script
response = generate_report(
    client_name="Carolina Padilla",
    period="",  # empty for all dates
    manager_name="David Salas",
    manager_email="dsf@protonmail.com",
    report_type="detailed, only completed"
)
print(response)
```

### Example System Response

```
Report sent to David Salas <d.salasforns@gmail.com>
```

The generated report will include a note at the end indicating the authorized recipient.

## 📂 Project Structure

```
.AI-Client-Agent-MCP/
├── .env                # Local environment variables (DB credentials, ports, etc.)
├── .dockerignore       # Files ignored by Docker during build
├── Dockerfile          # Instructions to build the application's Docker image
├── docker-compose.yml  # Docker services orchestration (app, db, pgadmin)
├── .cursor/            # Optional directory for Cursor IDE integration as an MCP 
│   └── ...             # This can be used to create AI-assisted prompts, workflows, and tools
├── backend/
│   ├── __init__.py
│   ├── server.py         # Entrypoint: FastMCP server runner
│   ├── mcp_instance.py   # Centralized MCP Agent instance
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── tools/      # MCP Tool definitions
│   │           ├── __init__.py
│   │           ├── client_tools.py
│   │           ├── invoice_tools.py
│   │           └── report_tools.py
│   ├── models/           # Pydantic models for validation and serialization
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── invoice.py
│   └── services/         # Business logic and database interaction
│       ├── __init__.py
│       ├── client_service.py   # Refactored with dependency injection for better testability
│       ├── invoice_service.py  # Refactored with dependency injection for better testability
│       └── report_service.py   # Service for report generation logic
├── database/
│   ├── create_tables.sql # SQL script to initialize DB schema (used by Docker)
│   └── managers.sql      # SQL script to create and populate the managers table
├── app_logs/             # Directory for application logs (created by Docker if mapped)
├── requirements.txt      # Python project dependencies
├── README.md             # This file
├── env.example           # Template for the .env file
├── pytest.ini            # Configuration for pytest and pytest-asyncio
└── tests/                # Test suite (configured with Pytest)
    ├── .env.test         # Environment variables for tests
    ├── conftest.py       # Pytest fixtures and configuration
    ├── __init__.py
    ├── unit/             # Unit tests
    └── integration/      # Integration tests
        ├── test_client_services.py  # Tests for client service functions
        └── test_invoice_services.py # Tests for invoice service functions
```

## 🗂️ Report History

All generated reports are stored in the `reports` table with the following fields:
- client_id, client_name (nullable for global reports)
- period (nullable)
- manager_email, manager_name
- report_type
- report_text (full report content)
- created_at

You can query the report history from the database or create a tool for this purpose.

## ⚠️ Security and Validation

- Only managers registered in the `managers` table can receive reports.
- The system always validates the recipient before sending any information.
- The recipient must be explicitly indicated in each request.
- The report and system response always show to whom it was sent.

## 🧪 Testing

The project is configured with `pytest` and includes comprehensive integration tests for services.

*   **Test Database Lifecycle**: 
    *   A separate test database (e.g., `ai_client_mcp_db_test` as configured in `tests/.env.test`) is automatically created if it doesn't exist before tests run.
    *   The schema from `database/create_tables.sql` is applied to this test database.
    *   Each test runs within its own database transaction, which is rolled back after the test completes, ensuring test isolation.
    *   The entire test database is automatically dropped after all tests in the session have finished.
    *   This lifecycle is managed by fixtures in `tests/conftest.py`.
*   **Service Architecture**:
    *   Service functions are designed with dependency injection, accepting an optional database connection parameter.
    *   This pattern allows tests to pass a controlled connection with transaction management.
    *   Makes it easy to test database operations with proper isolation.
*   **Test Environment Configuration**: The `tests/.env.test` file is used to configure the test database connection details, overriding any main `.env` settings for testing purposes.
*   **Fixtures**: `tests/conftest.py` contains crucial fixtures for managing the database connections, transactions, and the overall test database lifecycle.
*   **Run Tests**: From the project root (with the virtual environment activated, if not using Docker for testing):
    ```bash
    # Run all tests
    pytest
    
    # Run with verbose output
    pytest -v
    
    # Run only client service tests
    pytest tests/integration/test_client_services.py
    
    # Run only invoice service tests
    pytest tests/integration/test_invoice_services.py
    ```

## 🤝 Contributing

Contributions are welcome. Please follow standard development practices (fork, branch, PR) and consider adding tests for new features.

## 📄 License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for the full legal text and terms of use.

## 👤 Author

**David Salas**
- Website: [dasafodata.com](https://dasafodata.com)
- GitHub: [@dasafo](https://github.com/dasafo)
- LinkedIn: [David Salas](https://www.linkedin.com/in/dasafodata/)

<p align="center">
  <sub>Created with ❤️ by David Salas - dasafodata</sub>
</p>
