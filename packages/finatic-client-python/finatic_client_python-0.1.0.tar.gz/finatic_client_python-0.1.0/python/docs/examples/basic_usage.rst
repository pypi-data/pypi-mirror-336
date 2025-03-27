Basic Usage
==========

This guide covers the basic usage of the Finatic Python SDK.

Initialization
-------------

.. code-block:: python

   from finatic import Client

   # Initialize with your API key
   client = Client(api_key="your_api_key")

   # Or initialize with environment variable
   client = Client()  # Uses FINATIC_API_KEY environment variable

Authentication
-------------

.. code-block:: python

   # Set API key after initialization
   client.api_key = "your_api_key"

   # Check if authenticated
   if client.is_authenticated():
       print("Successfully authenticated!")
   else:
       print("Authentication failed")

Basic Operations
--------------

.. code-block:: python

   # Get user profile
   profile = client.get_profile()

   # Get account balance
   balance = client.get_balance()

   # Get positions
   positions = client.get_positions()

   # Get watchlist
   watchlist = client.get_watchlist()

Error Handling
-------------

.. code-block:: python

   from finatic.exceptions import FinaticError

   try:
       client.get_profile()
   except FinaticError as e:
       print(f"Error: {e.message}")
       print(f"Code: {e.code}")
   except Exception as e:
       print(f"Unexpected error: {e}") 