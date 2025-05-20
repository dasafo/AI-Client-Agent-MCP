import pytest
from backend.core.database import database
from backend.services.client_service import ClientService
from backend.models.client import ClientCreate
from backend.models.client_note import ClientNoteCreate


@pytest.mark.asyncio
async def test_add_and_list_client_notes(tmp_path, monkeypatch):
    # Setup: connect to test database
    await database.connect()
    pool = database._pool
    if pool is None:
        raise ValueError("Database pool is not initialized.")
    service = ClientService(pool)

    # Cleanup previo: eliminar cliente si ya existe
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM clients WHERE email = $1", "nota.test2@example.com")

    # Crear un cliente de prueba
    client_data = ClientCreate(
        name="Nota Test",
        email="nota.test2@example.com",
        phone="600000001",
        city="Notasville",
    )
    created = await service.create_client(client_data)
    client_id = created["id"]

    # Añadir una nota
    note_text = "Primera nota de prueba."
    note_obj = ClientNoteCreate(client_id=client_id, note=note_text)
    note = await service.add_note(note_obj)
    assert note["note"] == note_text
    assert note["client_id"] == client_id
    assert "created_at" in note

    # Añadir otra nota
    note2_text = "Segunda nota de prueba."
    note2_obj = ClientNoteCreate(client_id=client_id, note=note2_text)
    note2 = await service.add_note(note2_obj)
    assert note2["note"] == note2_text

    # Listar notas
    notes = await service.list_notes(client_id)
    assert len(notes) >= 2
    notas_textos = [n["note"] for n in notes]
    assert note_text in notas_textos
    assert note2_text in notas_textos

    # Cleanup: eliminar el cliente (cascade borra notas)
    await service.delete_client(client_id)
    await database.disconnect()
