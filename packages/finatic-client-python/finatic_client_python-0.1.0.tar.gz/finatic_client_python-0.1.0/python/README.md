# Finatic Python SDK

This is the official Python SDK for the Finatic Backend API.

## Installation

```bash
pip install finatic-client-python
```

## Usage

```python
from finatic_python import Finatic

# Initialize the client
finatic = Finatic.init("your-api-key", "your-api-secret")

# Get your holdings
holdings = await finatic.get_holdings()

# Place an order
order = {
    "symbol": "AAPL",
    "quantity": 1,
    "side": "buy",
    "type_": "market",
    "time_in_force": "day"
}
await finatic.place_order(order)
```

## Development

To set up the development environment:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .
```

## Requirements

- Python 3.8 or higher
- Rust toolchain (for development) 