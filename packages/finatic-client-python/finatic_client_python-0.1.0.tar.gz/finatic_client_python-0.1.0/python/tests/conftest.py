import pytest
import os

@pytest.fixture(autouse=True)
def mock_api_key():
    """Mock the API key for all tests."""
    os.environ['FINATIC_API_KEY'] = 'test_api_key'
    yield
    if 'FINATIC_API_KEY' in os.environ:
        del os.environ['FINATIC_API_KEY']

@pytest.fixture(autouse=True)
def mock_http_client(monkeypatch):
    """Mock the HTTP client for all tests."""
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

    async def mock_request(*args, **kwargs):
        raise Exception('Network error')

    import aiohttp
    monkeypatch.setattr(aiohttp.ClientSession, 'request', mock_request) 