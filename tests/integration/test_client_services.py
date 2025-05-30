# tests/integration/test_client_services.py
import pytest
from backend.services.client_service import create_client, get_client_by_id, delete_client, update_client
from backend.models.client import ClientUpdate
# Los modelos Pydantic como ClientCreate no son estrictamente necesarios aquí
# ya que las funciones de servicio refactorizadas toman argumentos directos.
# from backend.models.client import ClientCreate 

# Test de integración para el servicio de clientes
# Este test verifica la correcta funcionalidad de las operaciones de creación y recuperación de clientes
# usando la base de datos de prueba y transacciones

@pytest.mark.asyncio
async def test_create_and_get_client(db_conn): # db_conn es la conexión transaccional de la DB de prueba
    """
    Tests creating a client using the refactored service function 
    (which accepts db_conn), then retrieving it using the refactored 
    service function to verify its creation and data integrity.
    
    Prueba la creación de un cliente utilizando la función de servicio refactorizada
    (que acepta db_conn), luego lo recupera usando la función de servicio
    refactorizada para verificar su creación e integridad de datos.
    """
    # 1. Arrange: Define the client data
    # Preparación: Definimos los datos del cliente
    client_name = "Test User Three"
    client_city = "Integration Test City PT" # PT for "Post-Refactor"
    client_email = "testuser.three.pr@example.com"

    # 2. Act: Create the client using the service function
    # Acción: Creamos el cliente usando la función de servicio
    # La función create_client ahora espera los campos primero, luego la conexión opcional.
    created_client_dict = await create_client(client_name, client_city, client_email, conn=db_conn)
    
    # Verificamos que se creó correctamente
    assert created_client_dict is not None, "create_client did not return a dictionary"
    assert "id" in created_client_dict, "Client ID not found in the returned dictionary from create_client"
    client_id = created_client_dict["id"]

    # 3. Assert: Verify the created client and then retrieve and verify
    # Verificación: Comprobamos el cliente creado y luego lo recuperamos y verificamos
    
    # Verificamos los datos del cliente creado
    assert created_client_dict["name"] == client_name
    assert created_client_dict["city"] == client_city
    assert created_client_dict["email"] == client_email

    # Ahora, recupera el cliente usando el servicio get_client_by_id
    # La función get_client_by_id ahora espera el ID primero, luego la conexión opcional.
    retrieved_client_dict = await get_client_by_id(client_id, conn=db_conn)

    # Verificamos que el cliente recuperado coincide con el creado
    assert retrieved_client_dict is not None, "get_client_by_id did not return a dictionary for the created client"
    assert retrieved_client_dict["id"] == client_id
    assert retrieved_client_dict["name"] == client_name
    assert retrieved_client_dict["city"] == client_city
    assert retrieved_client_dict["email"] == client_email

@pytest.mark.asyncio
async def test_delete_client_success_and_error(db_conn):
    # Crear un cliente
    client = await create_client("Delete Test", "Test City", "delete@example.com", conn=db_conn)
    client_id = client["id"]
    # Borrar el cliente
    deleted = await delete_client(client_id, conn=db_conn)
    assert deleted is True
    # Intentar borrar de nuevo (debe fallar)
    deleted_again = await delete_client(client_id, conn=db_conn)
    assert deleted_again is False
    # Verificar que ya no existe
    assert await get_client_by_id(client_id, conn=db_conn) is None

@pytest.mark.asyncio
async def test_update_client_no_changes(db_conn):
    # Crear un cliente
    client = await create_client("Update No Change", "NoChange City", "nochange@example.com", conn=db_conn)
    client_id = client["id"]
    # Intentar actualizar sin cambios
    update_data = ClientUpdate()  # No fields set
    updated = await update_client(client_id, update_data, conn=db_conn)
    # Debe devolver el cliente original
    assert updated["id"] == client_id
    assert updated["name"] == client["name"]
    assert updated["city"] == client["city"]
    assert updated["email"] == client["email"] 