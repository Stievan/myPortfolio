

from stockClass import StockAccount, Stock
from datetime import datetime
import pandas as pd

account = StockAccount(1000, datetime(2023, 1, 1))
stock = Stock(100, "Stock A")
account.buy_stocks(stock, 50, 100, datetime(2023, 1, 15))
account.sell_stocks(stock, 50, 100, datetime(2023, 1, 30))

print(account.stocks)
