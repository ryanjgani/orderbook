# Matching Engine

The Matching Engine is a Python implementation of a basic order book for processing limit orders in a financial trading system.

Ryan Gani - ryanjgani@gmail.com

## Features

-   Supports limit order placement and execution.
-   Maintains separate buy and sell order books for each instrument.
-   Provides methods to cancel orders, retrieve the best bid and ask prices, retrieve the order book of a given instrument, and retrieve the executed trades for a specific instrument.

## Usage

1. Create an instance of the `OrderBook` class by providing a list of initial orders.
2. Use the `limit_order` method to process a limit order and match it with existing orders in the order book.
3. Use the `cancel_order` method to cancel an order from the order book.
4. Use the `get_best_bid` method to retrieve the best bid price for a given instrument.
5. Use the `get_best_ask` method to retrieve the best ask price for a given instrument.
6. Use the `print_order_book` method to print the order book for a given instrument.

## Example

```python
# Create an instance of the OrderBook
order_book = OrderBook([
    ('BTC', 'buy', 100.0, 10),
    ('BTC', 'buy', 99.0, 5),
    ('BTC', 'sell', 101.0, 7),
    ('BTC', 'sell', 102.0, 3),
])

# Place a limit order
order_book.limit_order('BTC', 'buy', 98.0, 8)

# Cancel an order
order_book.cancel_order('BTC', 100.0, 'buy')

# Retrieve best bid and ask prices
best_bid = order_book.get_best_bid('BTC')
best_ask = order_book.get_best_ask('BTC')

# Print the order book
order_book.print_order_book('BTC')
```
