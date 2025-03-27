from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class OrderSide(str, Enum):
    """Order side (buy or sell)."""
    BUY = "buy"
    SELL = "sell"

class OrderType(str, Enum):
    """Order type."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class TimeInForce(str, Enum):
    """Order time in force."""
    DAY = "day"
    GTC = "gtc"
    OPG = "opg"
    CLS = "cls"
    IOC = "ioc"
    FOK = "fok"

class Balance(BaseModel):
    """Account balance information."""
    cash: float
    buying_power: float
    equity: float
    long_market_value: float
    short_market_value: float
    initial_margin: float
    maintenance_margin: float
    last_equity: float

class Account(BaseModel):
    """Trading account information."""
    id: str
    name: str
    type_: str = Field(alias="type")
    status: str
    balance: Optional[Balance] = None

class Holding(BaseModel):
    """Position holding information."""
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float

class Order(BaseModel):
    """Order information."""
    symbol: str
    side: OrderSide
    quantity: float
    type_: OrderType = Field(alias="type")
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.DAY

class Portfolio(BaseModel):
    """Portfolio information."""
    total_value: float
    cash: float
    equity: float
    positions: List[Holding]

class Performance(BaseModel):
    """Portfolio performance metrics."""
    total_return: float
    daily_return: float
    weekly_return: float
    monthly_return: float
    yearly_return: float
    max_drawdown: float
    sharpe_ratio: float
    beta: float
    alpha: float

class Event(BaseModel):
    """API event information."""
    id: str
    type_: str = Field(alias="type")
    timestamp: datetime
    data: dict 