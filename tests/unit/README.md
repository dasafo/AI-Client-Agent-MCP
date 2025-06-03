# Unit Tests

This directory contains unit tests for individual components and functions of the application.

## Test Files

### `test_generate_report.py`
- Tests report generation functionality
- Mocks external dependencies (LLM, email)
- Verifies report content and formatting
- Tests error handling and validation

### `test_manager_service.py`
- Tests manager service functions
- Verifies manager CRUD operations
- Tests authorization logic
- Validates error handling

### `test_tools_logic.py`
- Tests core tool functionality
- Verifies input validation
- Tests error handling
- Validates tool responses

## Test Structure

Each test file follows this pattern:
1. Import necessary modules and fixtures
2. Define test cases
3. Mock external dependencies
4. Assert expected outcomes

## Example Test

```python
import pytest
from unittest.mock import AsyncMock, patch
from backend.api.v1.tools import report_tools

@pytest.mark.asyncio
async def test_generate_report_success():
    # Mock dependencies
    with patch('backend.api.v1.tools.report_tools.obtener_manager_autorizado', 
              new=AsyncMock(return_value={'name': 'Test Manager'})):
        # Test the function
        result = await report_tools.generate_report(
            client_name='Test Client',
            period='2024',
            manager_name='Test Manager',
            manager_email='test@example.com',
            report_type='general'
        )
        # Assert results
        assert result['success'] is True
```

## Best Practices

1. Mock external dependencies
2. Test both success and failure cases
3. Use descriptive test names
4. Keep tests focused and isolated
5. Follow the Arrange-Act-Assert pattern
6. Use appropriate fixtures 