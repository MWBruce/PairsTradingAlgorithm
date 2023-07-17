from OrderBook import OrderBook
from datetime import timedelta

class Market:
    def __init__(self, csv_name1, csv_name2):
        self.orderbook1 = OrderBook(csv_name1)
        self.orderbook2 = OrderBook(csv_name2)
        self.increment()
        self.start_time = min(self.orderbook1.get_time(), self.orderbook2.get_time())
        self.end_time = self.start_time

    def increment(self):
        if not self.is_market_open(): 
            return

        self.orderbook1.increment()
        if not self.orderbook1.is_open: 
            self.orderbook2.is_open = False 
            return

        self.orderbook2.increment()
        if not self.orderbook2.is_open: 
            self.orderbook1.is_open = False 
            return

        self.end_time = max(self.orderbook1.get_time(), self.orderbook2.get_time())


        while abs(self.get_time_diff().total_seconds()) >= 0.1:
            if self.orderbook1.get_time() < self.orderbook2.get_time():
                self.orderbook1.increment()
            else:
                self.orderbook2.increment()

    def get_time_diff(self):
        if not self.is_market_open(): 
            return timedelta(seconds=0)
        return self.orderbook1.get_time() - self.orderbook2.get_time()

    def get_current_bids(self):
        bid1 = self.orderbook1._bid[0] if len(self.orderbook1._bid) > 0 else None
        bid2 = self.orderbook2._bid[0] if len(self.orderbook2._bid) > 0 else None
        return [bid1, bid2]

    def get_current_asks(self):
        ask1 = self.orderbook1._ask[0] if len(self.orderbook1._ask) > 0 else None
        ask2 = self.orderbook2._ask[0] if len(self.orderbook2._ask) > 0 else None
        return [ask1, ask2]
    
    def is_market_open(self): 
        return self.orderbook1.is_open and self.orderbook2.is_open
    
    def get_elapsed_minutes(self):
        elapsed_time = self.end_time - self.start_time
        return elapsed_time.total_seconds() / 60
    
    def get_time(self):
        return self.end_time
