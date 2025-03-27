from typing import Optional, List, Dict, Any
from datetime import datetime

from .models import (
    Account,
    Holding,
    Order,
    Portfolio,
    Performance,
    Event,
)

class FinaticClient:
    """Rust-based Finatic client."""
    
    def __init__(self, api_key: str, base_url: str) -> None:
        """Initialize the client."""
        ...
    
    async def get_accounts(self) -> List[Account]:
        """Get all accounts."""
        ...
    
    async def get_holdings(self) -> List[Holding]:
        """Get all holdings."""
        ...
    
    async def place_order(self, order: Order) -> str:
        """Place an order."""
        ...
    
    async def get_portfolio(self) -> Portfolio:
        """Get portfolio."""
        ...
    
    async def get_performance(self) -> Performance:
        """Get performance metrics."""
        ...
    
    async def get_analytics(
        self,
        metrics: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get analytics data."""
        ...
    
    async def get_events(self, event_type: Optional[str] = None) -> List[Event]:
        """Get events."""
        ... 