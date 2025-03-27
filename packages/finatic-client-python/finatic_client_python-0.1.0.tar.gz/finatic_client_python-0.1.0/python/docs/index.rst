Welcome to Finatic Python SDK's documentation!
===========================================

The Finatic Python SDK provides a powerful and easy-to-use interface for integrating with Finatic's platform from Python applications.

Installation
-----------

.. code-block:: bash

   pip install finatic-client-python

Quick Start
----------

.. code-block:: python

   from finatic import Client

   # Initialize the client
   client = Client(api_key="your_api_key")

   # Get user data
   user_data = client.get_user_data()

   # Place a trade
   trade = client.place_trade(
       symbol="AAPL",
       quantity=10,
       side="buy"
   )

API Reference
------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/client
   api/models
   api/exceptions

Examples
--------

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   examples/basic_usage
   examples/advanced_features
   examples/error_handling

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 