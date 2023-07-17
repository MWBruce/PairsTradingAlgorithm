## source venv/bin/activate
## deactivate

from Account import Account
from Market import Market
from AutoTrader import AutoTrader
import os

os.system('clear')

# InvestmentAccount = Account(500)

# market = Market('Data/TestDataAAVE.csv', 'Data/TestDataUNI.csv') # Has 1999 valid orderbooks from 8:22:36 am to 8:46:20 am
market = Market('Data/AAVEUSDT_orderbook.csv', 'Data/UNIUSDT_orderbook.csv') # Has 50516 valid orderbooks from 8:22:36 am to 16:21:12

errCount = 0
unitsInSync = 0


autoTrader = AutoTrader(4000,0.04,500)

while(market.is_market_open()):
    AAVE_bid_price, AAVE_bid_units = map(float, market.get_current_bids()[0])
    AAVE_ask_price, AAVE_ask_units = map(float, market.get_current_asks()[0])
    UNI_bid_price, UNI_bid_units = map(float, market.get_current_bids()[1])
    UNI_ask_price, UNI_ask_units = map(float, market.get_current_asks()[1])

    autoTrader.GetInfo(market.get_time(), 
                       AAVE_bid_price, AAVE_bid_units, 
                       AAVE_ask_price, AAVE_ask_units, 
                       UNI_bid_price, UNI_bid_units, 
                       UNI_ask_price, UNI_ask_units)

    if abs(market.get_time_diff().total_seconds()) > 0.1:
        errCount = errCount + 1
    else:
        unitsInSync = unitsInSync + 1
    market.increment()

autoTrader.SellAll()
print(autoTrader.GetProfitOrLoss())

# print(errCount) ## Checking for periods where time difference is off
# print(unitsInSync) ## Checking for periods where time difference is on

# print(f"The market ran for {market.get_elapsed_minutes()} minutes.")

