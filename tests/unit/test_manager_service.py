import pytest
from unittest.mock import AsyncMock, patch
from backend.services import manager_service
from backend.models.manager import ManagerOut
import datetime

@pytest.mark.asyncio
async def test_get_manager_by_name_success():
    """
    Test the retrieval of a manager by name.
    """
    fake_row = {
        'id': 1,
        'name': 'David Salas',
        'email': 'dsf@protonmail.com',
        'role': 'boss',
        'created_at': datetime.datetime(2024, 1, 1, 12, 0, 0)
    }
    with patch('backend.core.database.Database.fetchrow', new=AsyncMock(return_value=fake_row)):
        result = await manager_service.get_manager_by_name('David Salas')
        assert result['name'] == 'David Salas'
        assert result['email'] == 'dsf@protonmail.com'
        assert result['role'] == 'boss'
        assert isinstance(result['created_at'], datetime.datetime)

@pytest.mark.asyncio
async def test_get_manager_by_name_not_found():
    """
    Test the retrieval of a manager that does not exist.
    """
    with patch('backend.core.database.Database.fetchrow', new=AsyncMock(return_value=None)):
        result = await manager_service.get_manager_by_name('No Existe')
        assert result is None

@pytest.mark.asyncio
async def test_get_manager_by_email_success():
    """
    Test the retrieval of a manager by email.
    """
    fake_row = {
        'id': 2,
        'name': 'Ana Ruiz',
        'email': 'ana.ruiz@dasafodata.com',
        'role': 'manager',
        'created_at': datetime.datetime(2024, 2, 2, 10, 0, 0)
    }
    with patch('backend.core.database.Database.fetchrow', new=AsyncMock(return_value=fake_row)):
        result = await manager_service.get_manager_by_email('ana.ruiz@dasafodata.com')
        assert result['name'] == 'Ana Ruiz'
        assert result['email'] == 'ana.ruiz@dasafodata.com'
        assert result['role'] == 'manager'

@pytest.mark.asyncio
async def test_list_managers_success():
    """
    Test the retrieval of all managers.
    """
    fake_rows = [
        {'id': 1, 'name': 'David Salas', 'email': 'dsf@protonmail.com', 'role': 'boss', 'created_at': datetime.datetime(2024, 1, 1, 12, 0, 0)},
        {'id': 2, 'name': 'Ana Ruiz', 'email': 'ana.ruiz@dasafodata.com', 'role': 'manager', 'created_at': datetime.datetime(2024, 2, 2, 10, 0, 0)}
    ]
    with patch('backend.core.database.Database.fetch', new=AsyncMock(return_value=fake_rows)):
        result = await manager_service.list_managers()
        assert len(result) == 2
        assert result[0]['name'] == 'David Salas'
        assert result[1]['email'] == 'ana.ruiz@dasafodata.com'

@pytest.mark.asyncio
async def test_list_managers_error():
    """
    Test the retrieval of all managers with an error.
    """
    with patch('backend.core.database.Database.fetch', new=AsyncMock(side_effect=Exception('DB error'))):
        result = await manager_service.list_managers()
        assert result == [] 