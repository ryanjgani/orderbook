import heapq

class OrderBook:
    def __init__(self, orders):
        """
        Initializes the OrderBook with a list of orders.

        Time Complexity: O(N log N), where N is the number of orders.
        """
        self.order_book = {}
        self.input_queue = [(instrument, side, price, quantity) for instrument, side, price, quantity in orders]
        self.output_queue = {}
        self._print_input_queue()

        for instrument, side, price, quantity in orders:
            self.limit_order(instrument, side, price, quantity)

    def limit_order(self, instrument, side, price, quantity):
        """
        Processes a limit order by matching it with existing orders in the order book.

        Time Complexity: O(M + N log N), where M is the number of matching orders and N is the number of orders in the order book for the given instrument and side.
        """
        if instrument not in self.order_book:
            self.order_book[instrument] = {'buy_orders': [], 'sell_orders': []}

        if side == 'buy':
            matching_orders = self.order_book[instrument]['sell_orders']
            match_condition = lambda order_price: order_price <= price
        elif side == 'sell':
            matching_orders = self.order_book[instrument]['buy_orders']
            match_condition = lambda order_price: order_price >= price

        matches = []
        while matching_orders and match_condition(matching_orders[0][0]):
            match = heapq.heappop(matching_orders)
            match_price, match_quantity = match
            if quantity >= match_quantity:
                quantity -= match_quantity
                matches.append((match_price, match_quantity))
            else:
                match_quantity -= quantity
                matches.append((match_price, quantity))
                heapq.heappush(matching_orders, (match_price, match_quantity))
                quantity = 0
                break

        if quantity > 0:
            if side == 'buy':
                message = f"Limit order: Side: BUY, Instrument: {instrument}, Price: {price}, Quantity: {quantity}"
                heapq.heappush(self.order_book[instrument]['buy_orders'], (-price, quantity))
            elif side == 'sell':
                message = f"Limit order: Side: SELL, Instrument: {instrument}, Price: {price}, Quantity: {quantity}"
                heapq.heappush(self.order_book[instrument]['sell_orders'], (price, quantity))
            self.output_queue[instrument] = self.output_queue.get(instrument, []) + [('LIMIT ORDER', message)]
            print(f"ACKNOWLEDGEMENT: {message}")
        if matches:
            self._print_executed_orders(instrument, side, price, matches)

    def _print_executed_orders(self, instrument, side, price, matches):
        """
        Prints the executed orders for a given instrument, side, price, and matches.

        Time Complexity: O(N), where N is the number of matches.
        """
        for match_price, match_quantity in matches:
            if side == 'buy':
                message = f"Buy order executed: Instrument: {instrument}, Price: {match_price}, Quantity: {match_quantity}"
            elif side == 'sell':
                message = f"Sell order executed: Instrument: {instrument}, Price: {match_price}, Quantity: {match_quantity}"
            self.output_queue[instrument] = self.output_queue.get(instrument, []) + [('EXECUTE', message)]
            print(f"ACKNOWLEDGEMENT: {message}")

    # Prints the input queue of orders.
    def _print_input_queue(self):
        print("---- Input Queue ----")
        for instrument, side, price, quantity in self.input_queue:
            print(f"Side: {side}, Instrument: {instrument} Price: {price}, Quantity: {quantity}")

    # Prints the output queue of orders of a given instrument.
    def _print_output_queue(self, instrument):
        print(f"---- Output Queue ({instrument}) ----")
        if instrument in self.output_queue:
            for action, message in self.output_queue[instrument]:
                print(f"{action} | {message}")
        
    # Cancels an order from the order book for a given instrument, price, and side.
    def cancel_order(self, instrument, price, side):
        if instrument in self.order_book:
            if side == 'buy':
                self.order_book[instrument]['buy_orders'] = [(p, q) for p, q in self.order_book[instrument]['buy_orders'] if p != -price]
                heapq.heapify(self.order_book[instrument]['buy_orders'])
            elif side == 'sell':
                self.order_book[instrument]['sell_orders'] = [(p, q) for p, q in self.order_book[instrument]['sell_orders'] if p != price]
                heapq.heapify(self.order_book[instrument]['sell_orders'])

    def get_best_bid(self, instrument):
        if instrument in self.order_book and self.order_book[instrument]['buy_orders']:
            return -self.order_book[instrument]['buy_orders'][0][0]  # Return the highest bid price
        else:
            return None

    def get_best_ask(self, instrument):
        if instrument in self.order_book and self.order_book[instrument]['sell_orders']:
            return self.order_book[instrument]['sell_orders'][0][0]  # Return the lowest ask price
        else:
            return None

    # prints the order book of a given instrument
    def print_order_book(self, instrument):
        if instrument in self.order_book:
            print(f"---- Order Book ({instrument}) ----")
            print("Buy Orders:")
            for price, quantity in self.order_book[instrument]['buy_orders']:
                print(f"Price: {abs(price)}, Quantity: {quantity}")
            print("Sell Orders:")
            for price, quantity in self.order_book[instrument]['sell_orders']:
                print(f"Price: {abs(price)}, Quantity: {quantity}")
            print("***************************************")
        else:
            print(f"No orders found for instrument: {instrument}")

# Example usage

# Add some orders for BTC and USDT
orders = [('BTC', 'buy', 50000, 1),
('BTC', 'sell', 51000, 3),
('BTC', 'buy', 52000, 1),
('USDT', 'buy', 49000, 10),
('USDT', 'sell', 49500, 8),
('USDT', 'buy', 50000, 5)]

order_book = OrderBook(orders)

# print orderbook for BTC
order_book.print_order_book('BTC')
order_book._print_output_queue('BTC')

# print orderbook for USDT
order_book.print_order_book('USDT')
order_book._print_output_queue('USDT')