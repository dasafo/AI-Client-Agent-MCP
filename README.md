# AI-Client-Agent-MCP

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Client management agent compatible with the MCP (Model Context Protocol).

## What is MCP and why use it?

**MCP (Model Context Protocol)** is an open protocol for tool-augmented AI agents. It allows agents (like Cursor, Claude, Windsurf, etc.) to interact with external tools and APIs in a standardized way. By using MCP, this project can be easily integrated with modern AI assistants and developer tools, enabling automation, advanced workflows, and seamless interoperability.

## ✨ Features

- ✅ Full client management (CRUD)
- 🚀 RESTful API based on FastAPI
- 🗃️ PostgreSQL database
- 🔄 Compatible with Cursor, Windsurf, Claude, and other modern MCP agents
- 📊 Data validation with Pydantic
- ⚡ Asynchronous and high performance

## ⚠️ Authentication Notice

**Authentication and authorization are NOT implemented in this demo.**

To add authentication, you could:
- Integrate OAuth2/JWT with FastAPI's security utilities
- Add API key checks in the MCP tool endpoints
- Use a reverse proxy (e.g., Traefik, Nginx) for access control

## 📦 Project Structure

```
AI-Client-Agent-MCP/
├── .env                    # Environment variables (create manually)
├── requirements.txt        # Python dependencies
├── backend/                # Backend source code
│   ├── __init__.py         # Python package
│   ├── server.py           # Application entry point
│   │
│   ├── api/               # API layer
│   │   └── tools/
│   │       └── client_tools.py  # MCP endpoints
│   │
│   ├── models/           # Data models
│   │   └── client.py       # Pydantic models
│   │
│   ├── services/         # Business logic
│   │   └── client_service.py
│   │
│   └── core/            # Utilities and config
│       ├── __init__.py
│       ├── config.py       # App configuration
│       └── database.py     # Database connection
└── README.md
```

## 🔄 Application Flow

1. `server.py` starts the MCP application
2. Requests arrive at endpoints in `api/tools/`
3. Tools use services for business logic
4. Services interact with the database
5. Models validate data at each step

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dasafo/AI-Client-Agent-MCP.git
   cd AI-Client-Agent-MCP
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the .env file:
   ```bash
   cp .env.example .env
   # Edit the .env file with your credentials
   ```

5. Start the server:
   ```bash
   python -m backend.server
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
# Application
APP_ENV=development
APP_DEBUG=True
APP_SECRET_KEY=your_secret_key_here

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name

# Connection URL (auto-generated)
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}:${POSTGRES_PORT}/${POSTGRES_DB}
```

## 🚀 Usage

### Run the server

```bash
python -m backend.server
```

### Run tests

```bash
pytest tests/
```

## 📚 Documentation

API docs will be available at `http://localhost:8000/docs` when the server is running.

## 🧪 Tests

- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Developed with ❤️ by David Salas
