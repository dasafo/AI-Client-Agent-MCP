# tests/integration/test_client_services.py
import pytest
from backend.services.client_service import create_client, get_client_by_id, delete_client, update_client
from backend.models.client import ClientUpdate
# Pydantic models like ClientCreate are not strictly necessary here
# since the refactored service functions take direct arguments.
# from backend.models.client import ClientCreate 

# Integration test for the client service
# This test verifies the correct functionality of client creation and retrieval operations
# using the test database and transactions

@pytest.mark.asyncio
async def test_create_and_get_client(db_conn): # db_conn is the transactional test DB connection
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
    created_client_dict = await create_client(client_name, client_city, client_email, conn=db_conn)
    
    # Verify it was created correctly
    assert created_client_dict is not None, "create_client did not return a dictionary"
    assert "id" in created_client_dict, "Client ID not found in the returned dictionary from create_client"
    client_id = created_client_dict["id"]

    # 3. Assert: Verify the created client and then retrieve and verify
    # Verify the created client data
    assert created_client_dict["name"] == client_name
    assert created_client_dict["city"] == client_city
    assert created_client_dict["email"] == client_email

    # Now, retrieve the client using the get_client_by_id service
    retrieved_client_dict = await get_client_by_id(client_id, conn=db_conn)

    # Verify the retrieved client matches the created one
    assert retrieved_client_dict is not None, "get_client_by_id did not return a dictionary for the created client"
    assert retrieved_client_dict["id"] == client_id
    assert retrieved_client_dict["name"] == client_name
    assert retrieved_client_dict["city"] == client_city
    assert retrieved_client_dict["email"] == client_email

@pytest.mark.asyncio
async def test_delete_client_success_and_error(db_conn):
    # Create a client
    client = await create_client("Delete Test", "Test City", "delete@example.com", conn=db_conn)
    client_id = client["id"]
    # Delete the client
    deleted = await delete_client(client_id, conn=db_conn)
    assert deleted is True
    # Try to delete again (should fail)
    deleted_again = await delete_client(client_id, conn=db_conn)
    assert deleted_again is False
    # Verify it no longer exists
    assert await get_client_by_id(client_id, conn=db_conn) is None

@pytest.mark.asyncio
async def test_update_client_no_changes(db_conn):
    # Create a client
    client = await create_client("Update No Change", "NoChange City", "nochange@example.com", conn=db_conn)
    client_id = client["id"]
    # Try to update with no changes
    update_data = ClientUpdate()  # No fields set
    updated = await update_client(client_id, update_data, conn=db_conn)
    # Should return the original client
    assert updated["id"] == client_id
    assert updated["name"] == client["name"]
    assert updated["city"] == client["city"]
    assert updated["email"] == client["email"] 