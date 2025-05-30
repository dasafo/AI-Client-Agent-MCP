# Quick Start Guide

This guide will help you set up and start developing with the AI Client Agent MCP project.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Docker and Docker Compose (optional, for containerized development)

## Setting Up Your Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Client-Agent-MCP.git
cd AI-Client-Agent-MCP
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
cp env.example .env
```

Edit the `.env` file to configure:
- Database connection details
- Server host and port
- Other application settings

### 5. Set Up the Database

#### Option A: Using Docker

The easiest way to get started is to use Docker Compose:

```bash
docker-compose up -d db
```

This will start a PostgreSQL container with the schema initialized.

#### Option B: Using a Local PostgreSQL Instance

If you have PostgreSQL installed locally:

1. Create a database:

```bash
createdb ai_client_mcp_db
```

2. Run the schema migration:

```bash
psql -U your_username -d ai_client_mcp_db -f database/create_tables.sql
```

### 6. Run the Application

#### Using Docker

```bash
docker-compose up -d
```

The application will be available at http://localhost:8000.

#### Locally

```bash
python -m backend.server
```

## Development Workflow

### Running Tests

```bash
# Create a test database (first time only)
createdb ai_client_mcp_db_for_tests

# Run tests
pytest
```

### Making Changes

1. Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes to the codebase
3. Run tests to ensure your changes don't break existing functionality:

```bash
pytest
```

4. Commit your changes:

```bash
git add .
git commit -m "Description of your changes"
```

5. Push your branch:

```bash
git push origin feature/your-feature-name
```

### Understanding the Codebase

The project follows a modular structure:

- `backend/core/`: Core infrastructure components (database, decorators, etc.)
- `backend/models/`: Data models using Pydantic
- `backend/services/`: Business logic for clients and invoices
- `backend/api/`: API tools for FastMCP integration
- `tests/`: Test suite for the application

## Key Development Patterns

### Database Connection Management

The project uses async PostgreSQL connections with connection pooling. Service functions are decorated with:

- `@with_db_connection`: For regular database operations
- `@db_transaction`: For operations that need transaction semantics

Example:

```python
from backend.core.decorators import with_db_connection

@with_db_connection
async def get_client(client_id: int, conn=None):
    return await conn.fetchrow("SELECT * FROM clients WHERE id = $1", client_id)
```

### Model Handling

Data validation and serialization is handled using Pydantic models:

```python
from backend.models.client import ClientCreate, ClientOut

@with_db_connection
async def create_client(client_data: dict, conn=None):
    # Validate input data
    client = ClientCreate(**client_data)
    
    # Insert into database
    query = """
    INSERT INTO clients (name, email, city) 
    VALUES ($1, $2, $3) 
    RETURNING id, name, email, city
    """
    row = await conn.fetchrow(query, client.name, client.email, client.city)
    
    # Return validated output
    return ClientOut(**dict(row)).dict()
```

## Common Tasks

### Adding a New Field to Clients

1. Update the database schema:
   - Add the field to the `clients` table in `database/create_tables.sql`
   - Apply the change to your development database

2. Update the models:
   - Add the field to `ClientBase`, `ClientCreate`, and `ClientOut` in `backend/models/client.py`

3. Update the service functions:
   - Modify queries in `backend/services/client_service.py` to include the new field

4. Update tests:
   - Update test cases in `tests/integration/test_client_services.py`

### Adding a New API Endpoint

1. Add a new tool function in `backend/api/client_tools.py` or `backend/api/invoice_tools.py`
2. Update the MCP registration in `backend/mcp_instance.py` to include the new tool

## Getting Help

- Refer to the documentation in the `docs/` directory
- Check the README files in each component directory
- Run tests with `-v` flag for more detailed output
- Review the codebase for similar patterns to follow 