from datetime import timedelta
from datetime import datetime

from Position import Position


class AutoTrader:
    def __init__(self, IndexMinutes,percent, Money):
        self.IndexedPrices = {
        "AAVE_bid_price": None,
        "AAVE_bid_units": None,
        "AAVE_ask_price": None,
        "AAVE_ask_units": None,
        "UNI_bid_price": None,
        "UNI_bid_units": None,
        "UNI_ask_price": None,
        "UNI_ask_units": None,
        "time": datetime.now()
        }
        self.CurrPrices = {
        "AAVE_bid_price": None,
        "AAVE_bid_units": None,
        "AAVE_ask_price": None,
        "AAVE_ask_units": None,
        "UNI_bid_price": None,
        "UNI_bid_units": None,
        "UNI_ask_price": None,
        "UNI_ask_units": None,
        "time": datetime.now()
        }
        self.percent = percent
        self.IndexInterval = IndexMinutes
        self.Money = Money
        self.StartingMoney = Money
        self.positions = []
        return

    def GetInfo(self, time, AaveBidPrice, AaveBidUnits, AaveAskPrice, AaveAskUnits, UniBidPrice, UniBidUnits, UniAskPrice, UniAskUnits):
        self.UpdateIndexes(time, AaveBidPrice, AaveBidUnits, AaveAskPrice, AaveAskUnits, UniBidPrice, UniBidUnits, UniAskPrice, UniAskUnits)
        self.check_positions()
        self.MakeCalculation()
        return

    def UpdateIndexes(self, time, AaveBidPrice, AaveBidUnits, AaveAskPrice, AaveAskUnits, UniBidPrice, UniBidUnits, UniAskPrice, UniAskUnits):
        if (self.IndexedPrices["AAVE_bid_price"] is None) or ((time - self.IndexedPrices["time"]) >= timedelta(minutes=self.IndexInterval)):
            self.IndexedPrices["AAVE_bid_price"] = AaveBidPrice
            self.IndexedPrices["AAVE_bid_units"] = AaveBidUnits
            self.IndexedPrices["AAVE_ask_price"] = AaveAskPrice
            self.IndexedPrices["AAVE_ask_units"] = AaveAskUnits
            self.IndexedPrices["UNI_bid_price"] = UniBidPrice
            self.IndexedPrices["UNI_bid_units"] = UniBidUnits
            self.IndexedPrices["UNI_ask_price"] = UniAskPrice
            self.IndexedPrices["UNI_ask_units"] = UniAskUnits
            self.IndexedPrices["time"] = time
        self.CurrPrices["AAVE_bid_price"] = AaveBidPrice
        self.CurrPrices["AAVE_bid_units"] = AaveBidUnits
        self.CurrPrices["AAVE_ask_price"] = AaveAskPrice
        self.CurrPrices["AAVE_ask_units"] = AaveAskUnits
        self.CurrPrices["UNI_bid_price"] = UniBidPrice
        self.CurrPrices["UNI_bid_units"] = UniBidUnits
        self.CurrPrices["UNI_ask_price"] = UniAskPrice
        self.CurrPrices["UNI_ask_units"] = UniAskUnits
        self.CurrPrices["time"] = time
        return
    
    def MakeCalculation(self):
        AAVE_movement = (self.CurrPrices["AAVE_bid_price"] - self.IndexedPrices["AAVE_bid_price"]) / self.IndexedPrices["AAVE_bid_price"]
        UNI_movement = (self.CurrPrices["UNI_bid_price"] - self.IndexedPrices["UNI_bid_price"]) / self.IndexedPrices["UNI_bid_price"]
        
        if abs(AAVE_movement - UNI_movement) > self.percent:
            self.ImplementPairStrategy(AAVE_movement, UNI_movement)
        return

    def ImplementPairStrategy(self, AAVE_movement, UNI_movement):
        trade_money = 500 ## $25 trades as the base point

        AAVE_price = self.CurrPrices["AAVE_bid_price"]
        UNI_price = self.CurrPrices["UNI_bid_price"]
        
        AAVE_units = trade_money / AAVE_price  
        UNI_units = trade_money / UNI_price 
        if AAVE_movement > UNI_movement:
            # print("AAVE has increased more than UNI")
            # print("Current AAVE ask price", self.CurrPrices["AAVE_ask_price"], "at time", self.CurrPrices["time"])
            # print("Compared to Indexed AAVE bid price", self.IndexedPrices["AAVE_bid_price"], "at time", self.IndexedPrices["time"])
            # print("Percentage change in AAVE price:", AAVE_movement * 100, "%")
            # print("Current UNI bid price", self.CurrPrices["UNI_bid_price"], "at time", self.CurrPrices["time"])
            # print("Compared to Indexed UNI bid price", self.IndexedPrices["UNI_bid_price"], "at time", self.IndexedPrices["time"])
            # print("Percentage change in UNI price:", UNI_movement * 100, "%")
            # print("Spread in price change:", (AAVE_movement - UNI_movement) * 100, "%")
            # print("\n")
            self.open_position(self.CurrPrices["time"], -AAVE_units, UNI_units)
        else:
            # print("UNI has increased more than AAVE")
            # print("Current UNI ask price", self.CurrPrices["UNI_ask_price"], "at time", self.CurrPrices["time"])
            # print("Compared to Indexed UNI bid price", self.IndexedPrices["UNI_bid_price"], "at time", self.IndexedPrices["time"])
            # print("Percentage change in UNI price:", UNI_movement * 100, "%")
            # print("Current AAVE bid price", self.CurrPrices["AAVE_bid_price"], "at time", self.CurrPrices["time"])
            # print("Compared to Indexed AAVE bid price", self.IndexedPrices["AAVE_bid_price"], "at time", self.IndexedPrices["time"])
            # print("Percentage change in AAVE price:", AAVE_movement * 100, "%")
            # print("Spread in price change:", (UNI_movement - AAVE_movement) * 100, "%")
            # print("\n")
            self.open_position(self.CurrPrices["time"], AAVE_units, -UNI_units)
        return
    
    def SellAll(self):
        for position in self.positions:
            self.close_position(position)
        self.positions = []

    def GetProfitOrLoss(self):
        return self.Money - self.StartingMoney
    
    def open_position(self, time, AAVE_units, UNI_units):
        AAVE_price = self.CurrPrices["AAVE_bid_price"]
        UNI_price = self.CurrPrices["UNI_bid_price"]
        # print("Openning Position, Balance Before Transaction: ", self.Money, " At Time: " , time)
        # print("AAVE  Current Price " ,  AAVE_price, "\nUNI Current Price: ", UNI_price)
        # print("AAVE  Indexed Price " ,  self.IndexedPrices["AAVE_bid_price"], "\nUNI Indexed Price: ", self.IndexedPrices["UNI_bid_price"])
        # print("AAVE Units: " ,  AAVE_units, "\nUNI Units: ", UNI_units)
        # print("AAVE Cost: " ,  AAVE_price * AAVE_units, "\nUNI Cost: ", UNI_price * UNI_units )
        self.Money -= AAVE_price * AAVE_units  
        self.Money -= UNI_price * UNI_units 
        position = Position(time, self.IndexedPrices["AAVE_bid_price"], self.IndexedPrices["UNI_bid_price"], AAVE_units, UNI_units, timedelta(minutes=self.IndexInterval))
        self.positions.append(position)
        # print("Balance After Transaction: ", self.Money, "\n" )
        return

    def close_position(self, position):
        time = self.CurrPrices["time"]
        AAVE_price = self.CurrPrices["AAVE_bid_price"]
        UNI_price = self.CurrPrices["UNI_bid_price"]
        
        position.close_position(time, AAVE_price, UNI_price)
        # print("Closing Position, Balance Before Transaction: ", self.Money, " At Time: " , time )
        # print("AAVE  Current Price " ,  AAVE_price, "\nUNI Current Price: ", UNI_price)
        # print("AAVE  Indexed Price " ,  self.IndexedPrices["AAVE_bid_price"], "\nUNI Indexed Price: ", self.IndexedPrices["UNI_bid_price"])
        # print("AAVE Units: " ,  position.AAVE_units , "\nUNI Units: ", position.UNI_units )
        # print("AAVE Cost: " ,  AAVE_price * position.AAVE_units, "\nUNI Cost: ", UNI_price * position.UNI_units )

        self.Money += AAVE_price * position.AAVE_units 
        self.Money += UNI_price * position.UNI_units 
        # print("Balance After Transaction: ", self.Money, "\n")
        self.positions.remove(position)
        return
    
    def check_positions(self):
        for position in self.positions:
            if not position.check_position(self.CurrPrices["time"], self.CurrPrices["AAVE_bid_price"], self.CurrPrices["UNI_bid_price"]):
                self.close_position(position)
        return