import asyncio
import os
import pytest
from backend.core.database import database
from backend.services.client_service import ClientService
from backend.models.client import ClientCreate


@pytest.mark.asyncio
async def test_create_and_get_client(tmp_path, monkeypatch):
    # Setup: connect to test database (assumes test DB is configured in .env)
    await database.connect()
    pool = database._pool
    if pool is None:
        raise ValueError("Database pool is not initialized.")
    service = ClientService(pool)

    # Create a new client
    client_data = ClientCreate(
        name="Alice Test",
        email="alice.test@example.com",
        phone="555123456",
        city="Testville",
    )
    created = await service.create_client(client_data)
    assert created["email"] == "alice.test@example.com"
    assert created["name"] == "Alice Test"

    # Retrieve the client by email
    fetched = await service.get_client_by_email("alice.test@example.com")
    assert fetched is not None
    assert fetched["name"] == "Alice Test"

    # Cleanup: remove the test client
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM clients WHERE email = $1", "alice.test@example.com"
        )
    await database.disconnect()
