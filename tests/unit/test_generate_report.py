import pytest
from unittest.mock import AsyncMock, patch
from backend.api.v1.tools import report_tools

@pytest.mark.asyncio
async def test_generate_report_success():
    # Mock manager autorizado
    fake_manager = {'name': 'David Salas', 'email': 'dsf@protonmail.com'}
    # Mock cliente y facturas
    fake_client = {'id': 1, 'name': 'Test Client'}
    fake_invoices = [
        {'id': 1, 'amount': 100, 'status': 'paid', 'issued_at': '2024-01-01'},
        {'id': 2, 'amount': 200, 'status': 'pending', 'issued_at': '2024-02-01'}
    ]
    # Mocks para sub-funciones
    with patch('backend.api.v1.tools.report_tools.obtener_manager_autorizado', new=AsyncMock(return_value=fake_manager)), \
         patch('backend.api.v1.tools.report_tools.obtener_invoices_cliente_periodo', new=AsyncMock(return_value=(fake_client, fake_invoices))), \
         patch('backend.api.v1.tools.report_tools.generar_texto_informe_llm', return_value='<b>Informe</b>'), \
         patch('backend.api.v1.tools.report_tools.send_email_with_report', new=AsyncMock(return_value=True)), \
         patch('backend.api.v1.tools.report_tools.guardar_informe_db', new=AsyncMock(return_value={"success": True})):
        result = await report_tools.generate_report(
            client_name='Test Client',
            period='2024',
            manager_name='David Salas',
            manager_email='dsf@protonmail.com',
            report_type='general'
        )
        assert result['success'] is True
        assert 'Informe enviado' in result['message']

@pytest.mark.asyncio
async def test_generate_report_manager_not_authorized():
    with patch('backend.api.v1.tools.report_tools.obtener_manager_autorizado', new=AsyncMock(return_value=None)):
        result = await report_tools.generate_report(
            client_name='Test Client',
            period='2024',
            manager_name='No Manager',
            manager_email='no@no.com',
            report_type='general'
        )
        assert result['success'] is False
        assert 'no autorizado' in result['error'].lower() 