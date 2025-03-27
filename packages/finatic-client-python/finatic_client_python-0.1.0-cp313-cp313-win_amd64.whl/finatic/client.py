from typing import Optional, List, Dict, Any
from datetime import datetime

from .models import (
    Account,
    Holding,
    Order,
    Portfolio,
    Performance,
    Event,
    OrderSide,
    OrderType,
    TimeInForce,
)
from .exceptions import FinaticError

class FinaticClient:
    """Main client for interacting with the Finatic API."""
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        sandbox: bool = False,
    ):
        """Initialize the Finatic client.
        
        Args:
            api_key: Your Finatic API key
            base_url: Optional custom base URL for the API
            sandbox: Whether to use the sandbox environment
        """
        self._client = self._create_client(api_key, base_url, sandbox)
    
    def _create_client(
        self,
        api_key: str,
        base_url: Optional[str],
        sandbox: bool,
    ) -> Any:
        """Create the underlying Rust client."""
        from ._core import FinaticClient as CoreClient
        
        if base_url is None:
            base_url = "https://sandbox-api.finatic.com" if sandbox else "https://api.finatic.com"
        
        return CoreClient(api_key, base_url)
    
    async def get_accounts(self) -> List[Account]:
        """Get all accounts associated with the API key."""
        try:
            return await self._client.get_accounts()
        except Exception as e:
            raise FinaticError(str(e)) from e
    
    async def get_holdings(self) -> List[Holding]:
        """Get all holdings across all accounts."""
        try:
            return await self._client.get_holdings()
        except Exception as e:
            raise FinaticError(str(e)) from e
    
    async def place_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        order_type: OrderType,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: TimeInForce = TimeInForce.DAY,
    ) -> str:
        """Place a new order.
        
        Args:
            symbol: The trading symbol
            side: Buy or sell
            quantity: Number of shares/contracts
            order_type: Market, limit, stop, or stop limit
            price: Required for limit and stop limit orders
            stop_price: Required for stop and stop limit orders
            time_in_force: Order time in force
            
        Returns:
            The order ID
        """
        try:
            order = Order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                type_=order_type,
                price=price,
                stop_price=stop_price,
                time_in_force=time_in_force,
            )
            return await self._client.place_order(order)
        except Exception as e:
            raise FinaticError(str(e)) from e
    
    async def get_portfolio(self) -> Portfolio:
        """Get the current portfolio state."""
        try:
            return await self._client.get_portfolio()
        except Exception as e:
            raise FinaticError(str(e)) from e
    
    async def get_performance(self) -> Performance:
        """Get portfolio performance metrics."""
        try:
            return await self._client.get_performance()
        except Exception as e:
            raise FinaticError(str(e)) from e
    
    async def get_analytics(
        self,
        metrics: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get analytics data.
        
        Args:
            metrics: List of metrics to retrieve
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            group_by: Optional grouping field
            
        Returns:
            Analytics data as a dictionary
        """
        try:
            return await self._client.get_analytics(
                metrics=metrics,
                start_date=start_date,
                end_date=end_date,
                group_by=group_by,
            )
        except Exception as e:
            raise FinaticError(str(e)) from e
    
    async def get_events(self, event_type: Optional[str] = None) -> List[Event]:
        """Get events from the API.
        
        Args:
            event_type: Optional event type filter
            
        Returns:
            List of events
        """
        try:
            return await self._client.get_events(event_type)
        except Exception as e:
            raise FinaticError(str(e)) from e 