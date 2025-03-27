import pytest
from finatic import FinaticClient, FinaticError

@pytest.fixture
def client():
    return FinaticClient(api_key="test_api_key")

@pytest.mark.asyncio
async def test_client_initialization(client):
    assert client.api_key == "test_api_key"

@pytest.mark.asyncio
async def test_client_error_handling(client):
    with pytest.raises(FinaticError) as exc_info:
        await client.get_user_data()
    assert "Authentication" in str(exc_info.value)

@pytest.mark.asyncio
async def test_client_rate_limiting(client):
    for _ in range(10):
        try:
            await client.get_user_data()
        except FinaticError as e:
            if "Rate limit" in str(e):
                return
    pytest.fail("Rate limiting not working as expected")

@pytest.mark.asyncio
async def test_client_request_retry(client):
    try:
        await client.get_user_data()
    except FinaticError as e:
        assert "Network" in str(e)

@pytest.mark.asyncio
async def test_client_trading(client):
    with pytest.raises(FinaticError):
        await client.place_order(
            symbol="AAPL",
            side="buy",
            quantity=1,
            order_type="market"
        )

@pytest.mark.asyncio
async def test_client_portfolio(client):
    with pytest.raises(FinaticError):
        await client.get_portfolio()

@pytest.mark.asyncio
async def test_client_analytics(client):
    with pytest.raises(FinaticError):
        await client.get_portfolio_analytics() 