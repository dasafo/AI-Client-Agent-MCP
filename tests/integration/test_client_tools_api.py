# tests/integration/test_client_tools_api.py
import pytest
from backend.api.v1.tools import client_tools

# Ensure conftest.py is set up with db_conn fixture for these tests

@pytest.mark.asyncio
async def test_create_get_delete_client_cycle(db_conn): # db_conn fixture from conftest.py
    # 1. Create Client
    create_response = await client_tools.create_client_tool(
        name="Integration Test Client", 
        city="Integration City", 
        email="integ.client@example.com"
    )
    assert create_response["success"], f"Create client failed: {create_response.get('error')}"
    created_client = create_response["client"]
    client_id = created_client["id"]
    assert created_client["name"] == "Integration Test Client"
    assert created_client["city"] == "Integration City"

    # 2. Get Client
    get_response = await client_tools.get_client(client_id=client_id)
    assert get_response["success"], f"Get client failed: {get_response.get('error')}"
    fetched_client = get_response["client"]
    assert fetched_client["id"] == client_id
    assert fetched_client["name"] == "Integration Test Client"

    # 3. Update Client
    update_response = await client_tools.update_client_tool(
        client_id=client_id,
        name="Updated Test Client",
        city="Updated City"
    )
    assert update_response["success"], f"Update client failed: {update_response.get('error')}"
    updated_client_from_response = update_response["client"]
    assert updated_client_from_response["name"] == "Updated Test Client"
    assert updated_client_from_response["city"] == "Updated City"

    # Verify update by getting again
    get_updated_response = await client_tools.get_client(client_id=client_id)
    assert get_updated_response["success"], f"Get updated client failed: {get_updated_response.get('error')}"
    fetched_updated_client = get_updated_response["client"]
    assert fetched_updated_client["name"] == "Updated Test Client"

    # 4. List Clients (basic check)
    list_response = await client_tools.list_clients()
    assert list_response["success"], f"List clients failed: {list_response.get('error')}"
    assert isinstance(list_response["clients"], list)
    # Check if our client is in the list (can be more specific)
    assert any(c["id"] == client_id for c in list_response["clients"])

    # 5. Delete Client
    delete_response = await client_tools.delete_client_tool(client_id=client_id)
    assert delete_response.success, f"Delete client failed: {delete_response.message}"
    assert delete_response.deleted_client["id"] == client_id

    # Verify deletion by trying to get again
    get_deleted_response = await client_tools.get_client(client_id=client_id)
    assert not get_deleted_response["success"], "Client was not actually deleted."
    assert "no encontrado" in get_deleted_response.get("error", "").lower()

@pytest.mark.asyncio
async def test_create_client_tool_only_name(db_conn):
    response = await client_tools.create_client_tool(name="Only Name Client")
    assert response["success"], f"Create client (only name) failed: {response.get('error')}"
    client = response["client"]
    assert client["name"] == "Only Name Client"
    assert client["city"] is None
    assert client["email"] is None
    # Cleanup (optional here as db_conn transaction will rollback, but good for clarity if needed elsewhere)
    if response["success"] and client.get("id"):
        await client_tools.delete_client_tool(client_id=client["id"])

# Add more integration tests for edge cases, error handling, etc. 