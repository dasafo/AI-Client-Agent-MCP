# tests/integration/test_invoice_services.py
import pytest
import pytest_asyncio
from datetime import date, timedelta
from decimal import Decimal

from backend.services.client_service import create_client
from backend.services.invoice_service import (
    create_invoice, 
    get_invoice_by_id,
    update_invoice,
    get_invoices_by_client_id,
    delete_invoice
)
from backend.models.invoice import InvoiceCreate, InvoiceUpdate

# Integration tests for the invoice service
# These tests verify the correct functionality of CRUD operations for invoices
# using the test database and transactions

@pytest.mark.asyncio
async def test_create_and_get_invoice(db_conn):
    """
    Test creating an invoice and retrieving it using the refactored service functions.
    This test also creates a client as a prerequisite.
    """
    # 1. Arrange: First create a client (needed for the invoice)
    client_name = "Invoice Test Client"
    client_city = "Invoice Test City"
    client_email = "invoice.test@example.com"
    
    created_client = await create_client(client_name, client_city, client_email, conn=db_conn)
    assert created_client is not None, "Failed to create client for invoice test"
    client_id = created_client["id"]
    
    # Create invoice data
    today = date.today()
    due_date = today + timedelta(days=30)
    invoice_data = InvoiceCreate(
        client_id=client_id,
        amount=Decimal("1250.50"),
        issued_at=today,
        due_date=due_date,
        status="pending"
    )
    
    # 2. Act: Create the invoice
    created_invoice = await create_invoice(invoice_data, conn=db_conn)
    
    # 3. Assert: Verify the invoice was created correctly
    assert created_invoice is not None, "create_invoice did not return a dictionary"
    assert "id" in created_invoice, "Invoice ID not found in the returned dictionary"
    invoice_id = created_invoice["id"]
    
    # Verify invoice data
    assert created_invoice["client_id"] == client_id
    assert created_invoice["amount"] == Decimal("1250.50")
    assert created_invoice["status"] == "pending"
    
    # Retrieve the invoice using get_invoice_by_id
    retrieved_invoice = await get_invoice_by_id(invoice_id, conn=db_conn)
    
    # Verify retrieved data
    assert retrieved_invoice is not None, "get_invoice_by_id did not return a dictionary"
    assert retrieved_invoice["id"] == invoice_id
    assert retrieved_invoice["client_id"] == client_id
    assert retrieved_invoice["amount"] == Decimal("1250.50")
    assert retrieved_invoice["status"] == "pending"
    assert retrieved_invoice["issued_at"] == today
    assert retrieved_invoice["due_date"] == due_date

@pytest.mark.asyncio
async def test_update_invoice(db_conn):
    """
    Test updating an invoice using the refactored update_invoice service function.
    """
    # 1. Arrange: Create a client and an invoice
    client = await create_client("Update Invoice Client", "Update City", "update.invoice@example.com", conn=db_conn)
    client_id = client["id"]
    
    today = date.today()
    original_due_date = today + timedelta(days=30)
    
    # Create the original invoice
    invoice_data = InvoiceCreate(
        client_id=client_id,
        amount=Decimal("500.00"),
        issued_at=today,
        due_date=original_due_date,
        status="pending"
    )
    
    original_invoice = await create_invoice(invoice_data, conn=db_conn)
    invoice_id = original_invoice["id"]
    
    # Prepare the update data - changing amount and status
    new_amount = Decimal("750.00")
    new_status = "paid"
    update_data = InvoiceUpdate(
        amount=new_amount,
        status=new_status
    )
    
    # 2. Act: Update the invoice
    updated_invoice = await update_invoice(invoice_id, update_data, conn=db_conn)
    
    # 3. Assert: Verify the update
    assert updated_invoice is not None, "update_invoice did not return a dictionary"
    assert updated_invoice["id"] == invoice_id
    assert updated_invoice["amount"] == new_amount, f"Amount not updated. Expected {new_amount}, got {updated_invoice['amount']}"
    assert updated_invoice["status"] == new_status, f"Status not updated. Expected {new_status}, got {updated_invoice['status']}"
    
    # Verify that client_id and other fields remain unchanged
    assert updated_invoice["client_id"] == client_id
    assert updated_invoice["issued_at"] == today
    assert updated_invoice["due_date"] == original_due_date

@pytest.mark.asyncio
async def test_get_invoices_by_client_id(db_conn):
    """
    Test retrieving all invoices for a specific client.
    """
    # 1. Arrange: Create a client and multiple invoices
    client = await create_client("Multiple Invoices Client", "Multiple City", "multiple.invoices@example.com", conn=db_conn)
    client_id = client["id"]
    
    today = date.today()
    
    # Create first invoice
    invoice1_data = InvoiceCreate(
        client_id=client_id,
        amount=Decimal("100.00"),
        issued_at=today,
        due_date=today + timedelta(days=15),
        status="pending"
    )
    await create_invoice(invoice1_data, conn=db_conn)
    
    # Create second invoice
    invoice2_data = InvoiceCreate(
        client_id=client_id,
        amount=Decimal("200.00"),
        issued_at=today,
        due_date=today + timedelta(days=30),
        status="pending"
    )
    await create_invoice(invoice2_data, conn=db_conn)
    
    # 2. Act: Retrieve invoices by client_id
    client_invoices = await get_invoices_by_client_id(client_id, conn=db_conn)
    
    # 3. Assert: Verify we got both invoices
    assert client_invoices is not None, "get_invoices_by_client_id did not return a list"
    assert isinstance(client_invoices, list), "The return value is not a list"
    assert len(client_invoices) == 2, f"Expected 2 invoices, got {len(client_invoices)}"
    
    # Check that both invoices have the correct client_id
    for invoice in client_invoices:
        assert invoice["client_id"] == client_id
    
    # Verify the amounts of the invoices (they should be different)
    invoice_amounts = [invoice["amount"] for invoice in client_invoices]
    assert Decimal("100.00") in invoice_amounts, "First invoice amount not found"
    assert Decimal("200.00") in invoice_amounts, "Second invoice amount not found"

@pytest.mark.asyncio
async def test_delete_invoice_success_and_error(db_conn):
    # Create client and invoice
    client = await create_client("Delete Invoice Client", "DelInv City", "delinv@example.com", conn=db_conn)
    client_id = client["id"]
    invoice_data = InvoiceCreate(client_id=client_id, amount=Decimal("100.00"))
    invoice = await create_invoice(invoice_data, conn=db_conn)
    invoice_id = invoice["id"]
    # Delete the invoice
    deleted = await delete_invoice(invoice_id, conn=db_conn)
    assert deleted is True
    # Try to delete again (should fail)
    deleted_again = await delete_invoice(invoice_id, conn=db_conn)
    assert deleted_again is False
    # Verify it no longer exists
    assert await get_invoice_by_id(invoice_id, conn=db_conn) is None

@pytest.mark.asyncio
async def test_update_invoice_no_changes(db_conn):
    # Create client and invoice
    client = await create_client("Update Invoice No Change", "NoChangeInv City", "nochangeinv@example.com", conn=db_conn)
    client_id = client["id"]
    invoice_data = InvoiceCreate(client_id=client_id, amount=Decimal("200.00"))
    invoice = await create_invoice(invoice_data, conn=db_conn)
    invoice_id = invoice["id"]
    # Try to update with no changes
    update_data = InvoiceUpdate()  # No fields set
    updated = await update_invoice(invoice_id, update_data, conn=db_conn)
    # Should return the original invoice
    assert updated["id"] == invoice_id
    assert updated["client_id"] == client_id
    assert updated["amount"] == invoice["amount"] 