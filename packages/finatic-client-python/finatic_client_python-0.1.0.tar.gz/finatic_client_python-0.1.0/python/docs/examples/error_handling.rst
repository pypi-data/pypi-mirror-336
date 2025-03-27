Error Handling
=============

This guide covers error handling in the Finatic Python SDK.

Exception Types
-------------

.. code-block:: python

   from finatic.exceptions import (
       FinaticError,
       AuthenticationError,
       RateLimitError,
       ValidationError,
       NetworkError
   )

   try:
       client.get_profile()
   except AuthenticationError:
       print("Invalid API key")
   except RateLimitError:
       print("Too many requests")
   except ValidationError:
       print("Invalid parameters")
   except NetworkError:
       print("Network connection issue")
   except FinaticError as e:
       print(f"Finatic error: {e.message}")

Retry Logic
----------

.. code-block:: python

   from finatic import Client
   from finatic.retry import RetryStrategy

   client = Client(api_key="your_api_key")
   retry = RetryStrategy(
       max_retries=3,
       backoff_factor=2,
       exceptions=(NetworkError, RateLimitError)
   )

   @retry
   def get_data():
       return client.get_profile()

   try:
       data = get_data()
   except Exception as e:
       print(f"Failed after retries: {e}")

Error Logging
------------

.. code-block:: python

   import logging
   from finatic import Client

   # Configure logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger('finatic')

   client = Client(api_key="your_api_key")

   try:
       client.get_profile()
   except Exception as e:
       logger.error(f"Error occurred: {e}", exc_info=True) 