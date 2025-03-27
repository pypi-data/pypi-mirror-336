Advanced Features
===============

This guide covers advanced features of the Finatic Python SDK.

WebSocket Connection
------------------

.. code-block:: python

   from finatic import Client
   import asyncio

   async def handle_trade(trade):
       print(f"New trade: {trade}")

   async def main():
       client = Client(api_key="your_api_key")
       
       # Connect to WebSocket
       await client.connect_websocket()
       
       # Subscribe to trade updates
       await client.subscribe_trades(handle_trade)
       
       # Keep the connection alive
       while True:
           await asyncio.sleep(1)

   asyncio.run(main())

Batch Operations
--------------

.. code-block:: python

   from finatic import Client

   client = Client(api_key="your_api_key")

   # Place multiple orders
   orders = [
       {"symbol": "AAPL", "quantity": 10, "side": "buy"},
       {"symbol": "GOOGL", "quantity": 5, "side": "sell"},
       {"symbol": "MSFT", "quantity": 15, "side": "buy"}
   ]

   results = client.place_orders(orders)

Rate Limiting
------------

.. code-block:: python

   from finatic import Client
   from finatic.rate_limit import RateLimiter

   client = Client(api_key="your_api_key")
   limiter = RateLimiter(client)

   # Make requests with rate limiting
   for i in range(100):
       with limiter:
           client.get_quote("AAPL") 