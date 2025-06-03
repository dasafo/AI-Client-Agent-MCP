# Dockerfile
# Configuration file to build the Docker image for the application

# Use an official Python image as the base
# Python 3.11-slim provides a good balance between size and functionality
FROM python:3.11-slim

# Set the working directory to /app inside the container
# All subsequent operations will be performed from this directory
WORKDIR /app

# Copy only the project configuration files first to leverage Docker cache
COPY pyproject.toml ./
COPY README.md ./
# (Opcional) Si usas poetry.lock, descomenta la siguiente línea:
# COPY poetry.lock ./

# Instala dependencias primero (esto se cachea mientras no cambien los archivos anteriores)
RUN pip install --no-cache-dir .

# Copy the rest of the application files to the /app working directory
# Only copy the necessary directories for execution
COPY ./backend ./backend
COPY ./database ./database
# Do not copy .env directly here; it will be handled via docker-compose.
# This improves security and flexibility, allowing different configurations per environment

# Expose the port where the FastMCP application runs (according to your .env it's 8000)
# This line is informative to document which port the application uses,
# although the actual port publishing is managed by docker-compose
EXPOSE 8000

# Command to run the application by executing the server script directly.
# This will allow FastMCP to start its own server (probably Uvicorn) as configured.
# The backend.server module contains the server initialization logic
CMD ["python", "-m", "backend.server"] 