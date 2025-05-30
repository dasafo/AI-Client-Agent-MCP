# tests/integration/test_client_services.py
import pytest
from backend.services.client_service import create_client, get_client_by_id
# Los modelos Pydantic como ClientCreate no son estrictamente necesarios aquí
# ya que las funciones de servicio refactorizadas toman argumentos directos.
# from backend.models.client import ClientCreate 

@pytest.mark.asyncio
async def test_create_and_get_client(db_conn): # db_conn es la conexión transaccional de la DB de prueba
    """
    Tests creating a client using the refactored service function 
    (which accepts db_conn), then retrieving it using the refactored 
    service function to verify its creation and data integrity.
    """
    # 1. Arrange: Define the client data
    client_name = "Test User Three"
    client_city = "Integration Test City PT" # PT for "Post-Refactor"
    client_email = "testuser.three.pr@example.com"

    # 2. Act: Create the client using the service function
    # La función create_client ahora espera los campos primero, luego la conexión opcional.
    created_client_dict = await create_client(client_name, client_city, client_email, conn=db_conn)
    
    assert created_client_dict is not None, "create_client did not return a dictionary"
    assert "id" in created_client_dict, "Client ID not found in the returned dictionary from create_client"
    client_id = created_client_dict["id"]

    # 3. Assert: Verify the created client and then retrieve and verify
    
    assert created_client_dict["name"] == client_name
    assert created_client_dict["city"] == client_city
    assert created_client_dict["email"] == client_email
    assert "created_at" in created_client_dict # También es bueno verificar que este campo existe

    # Ahora, recupera el cliente usando el servicio get_client_by_id
    # La función get_client_by_id ahora espera el ID primero, luego la conexión opcional.
    retrieved_client_dict = await get_client_by_id(client_id, conn=db_conn)

    assert retrieved_client_dict is not None, "get_client_by_id did not return a dictionary for the created client"
    assert retrieved_client_dict["id"] == client_id
    assert retrieved_client_dict["name"] == client_name
    assert retrieved_client_dict["city"] == client_city
    assert retrieved_client_dict["email"] == client_email
    assert retrieved_client_dict["created_at"] == created_client_dict["created_at"] # created_at debería ser el mismo 