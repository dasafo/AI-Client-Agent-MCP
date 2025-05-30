# AI Client Agent MCP Documentation

Welcome to the documentation for the AI Client Agent MCP project. This documentation provides comprehensive information about the system architecture, components, and development guidelines.

## Getting Started

- [Quick Start Guide](quickstart.md) - Set up your development environment and start working with the project
- [Project Overview](../README.md) - High-level overview of the project

## Architecture

- [Database Patterns](database_patterns.md) - Database connection management and transaction patterns
- [Core Components](../backend/core/README.md) - Documentation for core infrastructure components
- [Services](../backend/services/README.md) - Documentation for business logic services

## Development

- [Testing Guide](../tests/README.md) - Guide to running and writing tests
- [API Tools](../backend/api/README.md) - Documentation for API tools and endpoints

## Blog and Media

- [Blog Article](../blog_portfolio.md) - Detailed blog article about the project
- [LinkedIn Post](../linkedin_post.md) - LinkedIn post template for sharing the project

## Docker and Deployment

- [Docker Configuration](.dockerignore) - Docker build configuration
- [Environment Configuration](../env.example) - Environment variable configuration

## Contributing

We welcome contributions to the AI Client Agent MCP project! Please see the [README](../README.md) for more information on how to contribute.

## Project Structure

The project is organized into the following directories:

```
.
├── backend/           # Backend code
│   ├── api/           # API tools and endpoints
│   ├── core/          # Core infrastructure components
│   ├── models/        # Data models
│   ├── services/      # Business logic services
│   ├── mcp_instance.py # MCP instance definition
│   └── server.py      # Server entry point
├── database/          # Database schema and migrations
├── docs/              # Documentation
├── tests/             # Test suite
│   ├── integration/   # Integration tests
│   ├── unit/          # Unit tests
│   └── conftest.py    # Test fixtures
└── [other files]      # Configuration files, README, etc.
```

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 