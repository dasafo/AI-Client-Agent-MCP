# 🗂️ AI Client Agent MCP

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-15--alpine-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL 15-alpine">
  <img src="https://img.shields.io/badge/pgAdmin_4-latest-2496ED?style=for-the-badge&logo=pgadmin" alt="pgAdmin 4">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python" alt="Python 3.11">
</div>

<br>

> **AI Client Agent MCP** is a robust backend system for managing clients and their invoices (or quotes), designed to be operated by an AI Agent or programmatically. Built with FastAPI and PostgreSQL, and fully containerized for easy setup and deployment.

## 🎯 Core Features

*   👤 **Comprehensive Client Management**: CRUD (Create, Read, Update, Delete) operations for client profiles.
*   📄 **Invoice/Quote Administration**: Full CRUD operations for invoices, linked to clients, including status management (`pending`, `completed`, `canceled`).
*   🚀 **Asynchronous Performance**: Leverages `asyncio` and `asyncpg` for efficient, non-blocking database operations.
*   🛡️ **Rigorous Data Validation**: Employs Pydantic models to ensure data integrity across all interactions.
*   🤖 **MCP Tool Interface**: Exposes business logic through a set of tools for the Master Control Program, facilitating integration with AI agents and automated systems.
*   🐳 **Complete Dockerized Environment**: Includes the application, PostgreSQL database, and pgAdmin 4, all managed with Docker Compose for consistent and straightforward setup and execution.
*   ⚙️ **Flexible Configuration**: Environment variables for easy adaptation to different database setups and ports.
  

## 🚀 Quick Start (with Docker)

This is the recommended way to set up and run the project.

### 1. Prerequisites
*   [Docker](https://www.docker.com/get-started) installed.
*   Docker Compose (usually included with Docker Desktop; for Linux, install the `docker-compose-plugin`).

### 2. Installation

```bash
# 1. Clone the repository (if you haven't already)
git clone <repository_url>
cd AI-Client-Agent-MCP

# 2. Configure environment variables
# Copy env.example to .env if it's your first time, or ensure .env exists.
cp env.example .env 
# Edit .env with your configurations (see example below)
nano .env #(or your preferred editor)

# 3. Start all services
docker compose up --build
```

### 3. Essential Environment Variables (`.env`)

Your `.env` file should contain at least the following:

```env
# PostgreSQL Database Configuration
DB_USER=db_user
DB_PASSWORD=db_password
DB_NAME=AI-Agent-ddbb
DB_PORT=5432 # Internal port for PostgreSQL in its container

# Application Server Configuration
SERVER_PORT=8000 # Port on localhost to access the API

# pgAdmin 4 Configuration
PGADMIN_EMAIL=admin@example.com # Email for pgAdmin web interface login
PGADMIN_PASSWORD=admin          # Password for pgAdmin login
PGADMIN_PORT=5050         # Port on localhost to access pgAdmin
```
*Note: `DB_HOST` and `SERVER_HOST` are managed by Docker Compose for inter-container communication and host exposure.* 

### 4. Accessing Services

*   **API (AI Client Agent MCP)**: `http://localhost:${SERVER_PORT}` (e.g., `http://localhost:8000`)
*   **pgAdmin 4**: `http://localhost:${PGADMIN_PORT}` (e.g., `http://localhost:5050`)
    *   **pgAdmin Login**: Use `PGADMIN_EMAIL` and `PGADMIN_PASSWORD`.
    *   **Connect to Project DB from pgAdmin**:
        *   Host: `db` (Docker service name)
        *   Port: `5432` (PostgreSQL's internal port)
        *   Database: Your `DB_NAME`
        *   Username: Your `DB_USER`
        *   Password: Your `DB_PASSWORD`

### 5. Useful Docker Compose Commands

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

## 💡 Use Cases / Application Ideas

The `AI Client Agent MCP` can serve as a foundation for various automated systems:

*   **AI-Powered CRM**: An AI agent could use the tools to create and update clients based on email or chat interactions and draft invoices.
*   **Customer Support with Account Management**: Integrate with a ticketing system where an AI agent can query client information and recent invoices for more contextualized responses.
*   **Semi-Automated Billing Tool**: A simple interface (or bot) allowing non-technical users to request invoice creation for existing clients, with an AI agent validating or completing data.
*   **AI-Assisted Data Migration**: Use an agent to read data from a legacy system and utilize the `create_client` and `create_invoice` tools to populate this new system.

## 🛠️ MCP Tools (API Endpoints)

The application exposes its functionality through MCP tools. An MCP client can connect to the server (default: `http://localhost:${SERVER_PORT}/sse`) to invoke them.

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

## 📂 Detailed Project Structure

```
.AI-Client-Agent-MCP/
├── .env                # Local environment variables (DB credentials, ports, etc.)
├── .dockerignore       # Files ignored by Docker during build
├── Dockerfile          # Instructions to build the application's Docker image
├── docker-compose.yml  # Docker services orchestration (app, db, pgadmin)
├── backend/
│   ├── __init__.py
│   ├── server.py         # Entrypoint: FastAPI server and MCP runner
│   ├── mcp_instance.py   # Centralized MCP Agent instance
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── tools/      # MCP Tool definitions
│   │           ├── __init__.py
│   │           ├── client_tools.py
│   │           └── invoice_tools.py
│   ├── models/           # Pydantic models for validation and serialization
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── invoice.py
│   └── services/         # Business logic and database interaction
│       ├── __init__.py
│       ├── client_service.py
│       └── invoice_service.py
├── database/
│   └── create_tables.sql # SQL script to initialize DB schema (used by Docker)
├── app_logs/             # Directory for application logs (created by Docker if mapped)
├── requirements.txt      # Python project dependencies
├── README.md             # This file
├── env.example           # Template for the .env file
└── tests/                # Test suite (configured with Pytest)
    ├── .env.test         # Environment variables for tests
    ├── conftest.py       # Pytest fixtures and configuration
    ├── __init__.py
    ├── unit/             # Unit tests
    └── integration/      # Integration tests
```

## ⚙️ Local Development (Non-Docker Alternative)

For development or specific debugging scenarios outside Docker:

### Prerequisites (Local)
*   Python 3.11 (or the version in `Dockerfile`).
*   Locally accessible PostgreSQL server.

### Steps
1.  **Virtual Environment & Dependencies**: `python -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`.
2.  **Configure `.env`**: Ensure `DB_HOST` and `DB_PORT` point to your local PostgreSQL instance.
3.  **Manual Database Setup**: Create the database (`DB_NAME`) and run `psql -U ${DB_USER} -d ${DB_NAME} -a -f database/create_tables.sql`.
4.  **Run Application**: `python -m backend.server`.

## 🧪 Testing

The project is configured with `pytest`. Tests are organized into `unit/` and `integration/` directories within `tests/`.

*   **Test Environment Configuration**: The `tests/.env.test` file is used to configure a separate test database.
*   **Fixtures**: `tests/conftest.py` manages the creation and cleanup of the test database.
*   **Run Tests**: From the project root (with the virtual environment activated):
    ```bash
    pytest
    ```
    You can run specific tests or directories (e.g., `pytest tests/unit`).

## 🛡️ Security (Basic Considerations)

*   **Environment Variables**: Do not commit the `.env` file with actual credentials. Use `env.example` as a template.
*   **Strong Passwords**: Use robust passwords for the database and pgAdmin.
*   **Port Exposure**: `docker-compose.yml` exposes ports to `localhost`. For production, carefully review port exposure to external networks and configure firewalls.
*   **Dependencies**: Keep dependencies updated to mitigate known vulnerabilities.

## 🤝 Contributing

Contributions are welcome. Please follow standard development practices (fork, branch, PR) and consider adding tests for new features.

## 📄 License

MIT License

## 👤 Author

**David Salas**
- Website: [dasafodata.com](https://dasafodata.com)
- GitHub: [@dasafo](https://github.com/dasafo)
- LinkedIn: [David Salas](https://www.linkedin.com/in/dasafodata/)

---

<p align="center">
  <sub>Created with ❤️ by David Salas - dasafodata</sub>
</p>
