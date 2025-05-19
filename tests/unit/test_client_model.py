import pytest
from backend.models.client import ClientCreate


def test_client_create_model_valid():
    client = ClientCreate(
        name="John Doe", email="john@example.com", phone="123456789", city="New York"
    )
    assert client.name == "John Doe"
    assert client.email == "john@example.com"
    assert client.phone == "123456789"
    assert client.city == "New York"


def test_client_create_model_invalid_email():
    with pytest.raises(ValueError):
        ClientCreate(
            name="Jane Doe", email="not-an-email", phone="123456789", city="LA"
        )
