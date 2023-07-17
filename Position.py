from datetime import timedelta
from datetime import datetime

class Position:
    def __init__(self, time, AAVE_Price, UNI_Price, AAVE_units, UNI_units, expiryTime):
        self.start_time = time
        self.AAVE_start_price = AAVE_Price
        self.AAVE_units = AAVE_units
        self.UNI_start_price = UNI_Price
        self.UNI_units = UNI_units
        self.ExpiryTime = time + expiryTime


    def close_position(self, time, price1, price2):
        self.end_time = time
        self.AAVE_end_price = price1
        self.UNI_end_price = price2

    
    def check_position(self, time, AAVE_Price, UNI_Price):
        if time > self.ExpiryTime:
            print("Exiting due to time")
            return False
        AppropriateIndex = self.AAVE_units < self.UNI_units
        AAVE_Change = (AAVE_Price - self.AAVE_start_price)/self.AAVE_start_price
        UNI_Change = (UNI_Price - self.UNI_start_price)/self.UNI_start_price
        calculation = [AAVE_Change,UNI_Change]
        # print("Checking position with start prices: AAVE - ", self.AAVE_start_price, ", UNI - ", self.UNI_start_price)
        # print("Current prices: AAVE - ", AAVE_Price, ", UNI - ", UNI_Price)
        # print("Price changes: AAVE - ", AAVE_Change, ", UNI - ", UNI_Change)
        # print("Returning: ", calculation[AppropriateIndex] >= calculation[not AppropriateIndex], "\n")

        # if not (calculation[AppropriateIndex] <= calculation[not AppropriateIndex]):
        #     print("Exiting due to calculation")
        return (calculation[AppropriateIndex] <= calculation[not AppropriateIndex])
