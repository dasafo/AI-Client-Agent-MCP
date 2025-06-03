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

## 📚 Table of Contents

- [🗂️ AI Client Agent MCP](#️-ai-client-agent-mcp)
  - [📚 Table of Contents](#-table-of-contents)
  - [📂 Project Structure](#-project-structure)
  - [🛠️ Requirements and Tools](#️-requirements-and-tools)
    - [Prerequisites](#prerequisites)
    - [Development Tools](#development-tools)
  - [🚀 Installation and Setup](#-installation-and-setup)
    - [Docker Installation (Recommended)](#docker-installation-recommended)
    - [Local Installation with Poetry](#local-installation-with-poetry)
    - [Local Installation with pip](#local-installation-with-pip)
  - [💻 Usage and Execution](#-usage-and-execution)
    - [Accessing Services](#accessing-services)
    - [Useful Docker Commands](#useful-docker-commands)
  - [🧪 Testing and Code Quality](#-testing-and-code-quality)
    - [Running Tests](#running-tests)
    - [Code Quality Checks](#code-quality-checks)
  - [📚 Documentation and References](#-documentation-and-references)
    - [MCP Tools](#mcp-tools)
      - [Client Tools](#client-tools)
      - [Invoice Tools](#invoice-tools)
  - [💡 Use Cases and Examples](#-use-cases-and-examples)
    - [Example Interaction](#example-interaction)
      - [Natural Language Request](#natural-language-request)
      - [Structured Tool Call](#structured-tool-call)
  - [⚠️ Security, Limitations and Roadmap](#️-security-limitations-and-roadmap)
    - [Security Notes](#security-notes)
    - [Current Limitations](#current-limitations)
    - [Future Improvements](#future-improvements)
  - [🤝 Contributing and License](#-contributing-and-license)
  - [👤 Author and Contact](#-author-and-contact)

## 📂 Project Structure

```
.AI-Client-Agent-MCP/
├── .env                # Local environment variables (DB credentials, ports, etc.)
├── .dockerignore       # Files ignored by Docker during build
├── Dockerfile          # Instructions to build the application's Docker image
├── docker-compose.yml  # Docker services orchestration (app, db, pgadmin)
├── .cursor/            # Optional directory for Cursor IDE integration as an MCP 
│   └── ...             # This can be used to create AI-assisted prompts, workflows, and tools
├── pyproject.toml      # Project configuration and dependencies
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
├── README.md             # This file
├── env.example           # Template for the .env file
└── tests/                # Test suite (configured with Pytest)
    ├── .env.test         # Environment variables for tests
    ├── conftest.py       # Pytest fixtures and configuration
    ├── __init__.py
    ├── unit/             # Unit tests
    └── integration/      # Integration tests
        ├── test_client_services.py  # Tests for client service functions
        └── test_invoice_services.py # Tests for invoice service functions
```

## 🛠️ Requirements and Tools

### Prerequisites
*   Python 3.11 or higher
*   [Poetry](https://python-poetry.org/) (recommended) or pip
*   PostgreSQL 15 or higher
*   [Docker](https://www.docker.com/get-started) and Docker Compose

### Development Tools
The project uses several tools to maintain code quality, all configured in `pyproject.toml`:

*   **Black**: Code formatting
*   **isort**: Import sorting
*   **Ruff**: Fast Python linter
*   **MyPy**: Static type checking
*   **pre-commit**: Git hooks for code quality

These tools are configured in:
- `pyproject.toml`: Main configuration for all tools and dependencies
- `.pre-commit-config.yaml`: Git hooks configuration

## 🚀 Installation and Setup

### Docker Installation (Recommended)

```bash
# 1. Clone the repository
git clone <repository_url>
cd AI-Client-Agent-MCP

# 2. Configure environment variables
cp env.example .env 
# Edit .env with your configurations
nano .env #(or your preferred editor)

# 3. Start all services
docker compose up --build
```

### Local Installation with Poetry

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install
```

### Local Installation with pip

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using pip and pyproject.toml
pip install .

# Install pre-commit hooks
pre-commit install
```

## 💻 Usage and Execution

### Accessing Services

*   **MCP Server**: Connect via an MCP client (e.g., Cursor IDE) to the agent
*   **pgAdmin 4**: `http://localhost:${PGADMIN_PORT:-5050}`
    *   Login with `PGADMIN_EMAIL` and `PGADMIN_PASSWORD`
    *   Connect to DB using:
        *   Host: `db`
        *   Port: `5432`
        *   Database: Your `DB_NAME`
        *   Username: Your `DB_USER`
        *   Password: Your `DB_PASSWORD`

### Useful Docker Commands

```bash
# Start services
docker compose up --build

# Stop services
docker compose down

# View logs
docker compose logs -f

# Check status
docker compose ps

# Access app shell
docker compose exec app /bin/sh

# Access DB shell
docker compose exec db psql -U ${DB_USER} -d ${DB_NAME}
```

## 🧪 Testing and Code Quality

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/unit/test_generate_report.py

# Run tests with specific marker
pytest -m "integration"
```

### Code Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Run linter
ruff check .

# Type checking
mypy .
```

## 📚 Documentation and References

### MCP Tools

The application exposes its functionality through FastMCP tools:

#### Client Tools
*   `list_clients`: Lists all clients
*   `get_client(client_id: int)`: Retrieves a specific client
*   `create_client(name: str, city: Optional[str], email: Optional[str])`: Creates a new client
*   `update_client(client_id: int, name: Optional[str], city: Optional[str], email: Optional[str])`: Updates a client
*   `delete_client(client_id: int)`: Deletes a client

#### Invoice Tools
*   `list_invoices`: Lists all invoices
*   `get_invoice(invoice_id: int)`: Retrieves a specific invoice
*   `list_client_invoices(client_id: int)`: Lists all invoices for a specific client
*   `create_invoice(client_id: int, amount: str, issued_at: Optional[str], due_date: Optional[str], status: Optional[str])`: Creates an invoice
*   `update_invoice(invoice_id: int, client_id: Optional[str], amount: Optional[str], issued_at: Optional[str], due_date: Optional[str], status: Optional[str])`: Updates an invoice
*   `delete_invoice(invoice_id: int)`: Deletes an invoice

## 💡 Use Cases and Examples

### Example Interaction

#### Natural Language Request
> "Give me a detailed report of all completed quotes for client Carolina Padilla and send it to David Salas."

#### Structured Tool Call
```python
response = generate_report(
    client_name="Carolina Padilla",
    period="",  # empty for all dates
    manager_name="David Salas",
    manager_email="dsf@protonmail.com",
    report_type="detailed, only completed",
    api_token="changeme-token-dev"  # Must match REPORT_API_TOKEN
)
```

## ⚠️ Security, Limitations and Roadmap

### Security Notes
- Only managers registered in the `managers` table can receive reports
- The system validates the recipient before sending any information
- The recipient must be explicitly indicated in each request
- Reports always show to whom they were sent

### Current Limitations
- No configurable state transitions for invoices
- No detailed audit logs for invoice modifications
- Manual schema changes require database recreation

### Future Improvements
- Implement state transition logic
- Add audit logging
- Integrate migration tools (e.g., Alembic)

## 🤝 Contributing and License

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

This project is licensed under the [MIT License](LICENSE).

## 👤 Author and Contact

**David Salas**
- Website: [dasafodata.com](https://dasafodata.com)
- GitHub: [@dasafo](https://github.com/dasafo)
- LinkedIn: [David Salas](https://www.linkedin.com/in/dasafodata/)

<p align="center">
  <sub>Created with ❤️ by David Salas - dasafodata</sub>
</p>
