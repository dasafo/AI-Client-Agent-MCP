import pytest
from backend.core.database import database
from backend.services.client_service import ClientService
from backend.models.client import ClientCreate, ClientUpdate


@pytest.mark.asyncio
async def test_update_and_delete_client(tmp_path, monkeypatch):
    # Setup: connect to test database
    await database.connect()
    pool = database._pool
    if pool is None:
        raise ValueError("Database pool is not initialized.")
    service = ClientService(pool)

    # Crear un cliente de prueba
    client_data = ClientCreate(
        name="Bob Test",
        email="bob.test@example.com",
        phone="555987654",
        city="Testopolis",
    )
    created = await service.create_client(client_data)
    client_id = created["id"]

    # Actualizar el cliente
    update_data = ClientUpdate(
        name="Bob Updated",
        email="bob.test@example.com",
        phone="555987654",
        city="Ciudad Nueva",
    )
    updated = await service.update_client(client_id, update_data)
    assert updated is not None, "update_client returned None"
    assert updated["name"] == "Bob Updated"
    assert updated["city"] == "Ciudad Nueva"
    assert updated["email"] == "bob.test@example.com"

    # Intentar actualizar con email duplicado
    # Crear otro cliente
    other = await service.create_client(
        ClientCreate(
            name="Otro",
            email="otro@example.com",
            phone="555000000",
            city="Otra Ciudad",
        )
    )
    with pytest.raises(ValueError):
        await service.update_client(
            client_id,
            ClientUpdate(
                name="Bob Updated",
                email="otro@example.com",
                phone="555987654",
                city="Ciudad Nueva",
            ),
        )

    # Eliminar el cliente
    deleted = await service.delete_client(client_id)
    assert deleted is True
    # Verificar que ya no existe
    assert await service.get_client_by_id(client_id) is None

    # Cleanup: eliminar el otro cliente
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM clients WHERE email = $1", "otro@example.com")
    await database.disconnect()
