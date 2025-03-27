import pytest
from blindml.client import BlindML
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    return BlindML()

def test_init(client):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_zip_content"
        mock_get.return_value = mock_response

        client.init("https://fake-server.com", "fake-api-key")
        assert client.server_url == "https://fake-server.com"
        assert client.api_key == "fake-api-key"

def test_makekey(client):
    client.fhemodel_client = MagicMock()
    client.fhemodel_client.get_serialized_evaluation_keys.return_value = b"fake_key"
    key = client.makekey()
    assert key == b"fake_key"

def test_encode(client):
    client.fhemodel_client = MagicMock()
    client.fhemodel_client.quantize_encrypt_serialize.return_value = b"fake_encrypted_data"
    data = client.encode("input_data")
    assert data == b"fake_encrypted_data"
