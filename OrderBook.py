import pandas as pd
import numpy as np
from datetime import datetime
import ast

class OrderBook:
    def __init__(self, csv_name):
        self._feed = pd.read_csv(csv_name)
        self._current_row = -1
        self._bid = np.zeros((10, 2))
        self._ask = np.zeros((10, 2))
        self.is_open = True 
        

    def increment(self):
        self._current_row += 1
        if self._current_row < len(self._feed):

            current_row_data = self._feed.iloc[self._current_row]
            raw_bid = ast.literal_eval(current_row_data[1])[:10]
            raw_ask = ast.literal_eval(current_row_data[2])[:10]
            self._bid = np.array(raw_bid)
            self._ask = np.array(raw_ask)
        else:
            self._bid = np.zeros((10, 2))
            self._ask = np.zeros((10, 2))
            self.is_open = False 
            return

    def print_order_book(self):
        print("Bid Orders")
        for i in range(len(self._bid)):
            print(f"Price: {self._bid[len(self._bid) - i-1][0]}, Size: {self._bid[len(self._bid) -i-1][1]}")

        print("--------------------------------------------")

        for i in range(len(self._ask)):
            print(f"Price: {self._ask[i][0]}, Size: {self._ask[i][1]}")
        print("Ask Orders\n")
        return
    def get_time(self):
        date_str = self._feed.iloc[self._current_row][3]
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S:%f")
