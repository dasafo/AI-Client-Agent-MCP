# tests/integration/test_invoice_tools_api.py
import pytest
from backend.api.v1.tools import invoice_tools, client_tools
from decimal import Decimal

# Ensure conftest.py is set up with db_conn fixture for these tests

@pytest.fixture
async def test_client(db_conn): # Depends on db_conn to ensure it uses the test DB transaction
    """Fixture to create a client for invoice tests."""
    response = await client_tools.create_client_tool(name="Invoice Test Client", city="Invoice City")
    assert response["success"], "Failed to create client for invoice tests"
    client_data = response["client"]
    yield client_data # provide the client data to the test
    # Cleanup of client will be handled by transaction rollback via db_conn 
    # or if specific cleanup is needed and not relying on rollback:
    # await client_tools.delete_client_tool(client_id=client_data["id"])

@pytest.mark.asyncio
async def test_create_get_delete_invoice_cycle(db_conn, test_client):
    client_id = test_client["id"]

    # 1. Create Invoice
    create_response = await invoice_tools.create_invoice_tool(
        client_id=client_id,
        amount="123.45",
        issued_at="2023-01-15",
        due_date="2023-02-15",
        status="pending"
    )
    assert create_response["success"], f"Create invoice failed: {create_response.get('error')}"
    created_invoice = create_response["invoice"]
    invoice_id = created_invoice["id"]
    assert created_invoice["client_id"] == client_id
    assert Decimal(created_invoice["amount"]) == Decimal("123.45")
    assert created_invoice["status"] == "pending"

    # 2. Get Invoice
    get_response = await invoice_tools.get_invoice(invoice_id=invoice_id)
    assert get_response["success"], f"Get invoice failed: {get_response.get('error')}"
    fetched_invoice = get_response["invoice"]
    assert fetched_invoice["id"] == invoice_id
    assert Decimal(fetched_invoice["amount"]) == Decimal("123.45")

    # 3. Update Invoice
    update_response = await invoice_tools.update_invoice_tool(
        invoice_id=invoice_id,
        amount="150.00",
        status="pagado"
    )
    assert update_response["success"], f"Update invoice failed: {update_response.get('error')}"
    updated_invoice_from_resp = update_response["invoice"]
    assert Decimal(updated_invoice_from_resp["amount"]) == Decimal("150.00")
    assert updated_invoice_from_resp["status"] == "pagado"

    # Verify update by getting again
    get_updated_response = await invoice_tools.get_invoice(invoice_id=invoice_id)
    fetched_updated_invoice = get_updated_response["invoice"]
    assert Decimal(fetched_updated_invoice["amount"]) == Decimal("150.00")
    assert fetched_updated_invoice["status"] == "pagado"

    # 4. List Invoices (basic check)
    list_all_response = await invoice_tools.list_invoices()
    assert list_all_response["success"]
    assert any(inv["id"] == invoice_id for inv in list_all_response["invoices"])

    # 5. List Client Invoices
    list_client_inv_response = await invoice_tools.list_client_invoices(client_id=client_id)
    assert list_client_inv_response["success"]
    assert any(inv["id"] == invoice_id for inv in list_client_inv_response["invoices"])
    assert all(inv["client_id"] == client_id for inv in list_client_inv_response["invoices"])

    # 6. Delete Invoice
    delete_response = await invoice_tools.delete_invoice_tool(invoice_id=invoice_id)
    assert delete_response.success, f"Delete invoice failed: {delete_response.message}"
    assert delete_response.deleted_invoice["id"] == invoice_id

    # Verify deletion
    get_deleted_response = await invoice_tools.get_invoice(invoice_id=invoice_id)
    assert not get_deleted_response["success"]
    assert "no encontrada" in get_deleted_response.get("error", "").lower()

# Add more integration tests for specific error conditions, default values, etc. 