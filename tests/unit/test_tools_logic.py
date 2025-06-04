import pytest
from backend.api.v1.tools import report_tools

def test_build_report_prompt_basic():
    """
    Test the basic prompt building for a report.
    """
    invoices = [
        {'id': 1, 'amount': 100, 'status': 'paid', 'issued_at': '2024-01-01'},
        {'id': 2, 'amount': 200, 'status': 'pending', 'issued_at': '2024-02-01'}
    ]
    prompt = report_tools.build_report_prompt(
        invoices, client_name='Test Client', period='2024', report_type='general', manager_name='Manager', manager_email='manager@example.com'
    )
    assert 'Test Client' in prompt
    assert '2024' in prompt
    assert 'ID: 1' in prompt
    assert 'ID: 2' in prompt
    assert 'Manager' in prompt
    assert 'manager@example.com' in prompt
    assert '<html>' not in prompt  # No HTML tags, just instructions

def test_clean_llm_html_removes_script():
    """
    Test the cleaning of HTML content from scripts.
    """
    html = '<div>Hello<script>alert(1)</script>World</div>'
    cleaned = report_tools.clean_llm_html(html)
    assert '<script>' not in cleaned
    assert 'alert(1)' not in cleaned
    assert 'Hello' in cleaned and 'World' in cleaned

def test_clean_llm_html_removes_onclick():
    """
    Test the cleaning of HTML content from onclick events.
    """
    html = '<button onclick="evil()">Click</button>'
    cleaned = report_tools.clean_llm_html(html)
    assert 'onclick' not in cleaned
    assert 'Click' in cleaned

def test_clean_llm_html_removes_iframe():
    """
    Test the cleaning of HTML content from iframe tags.
    """
    html = '<iframe src="evil.com"></iframe>Safe'
    cleaned = report_tools.clean_llm_html(html)
    assert '<iframe' not in cleaned
    assert 'Safe' in cleaned

def test_clean_llm_html_removes_javascript_href():
    """
    Test the cleaning of HTML content from javascript: hrefs.
    """
    html = '<a href="javascript:evil()">link</a>'
    cleaned = report_tools.clean_llm_html(html)
    assert 'javascript:' not in cleaned
    assert 'link' in cleaned 