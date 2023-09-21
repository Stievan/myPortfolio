import sys
sys.path.append('C:\\Projekte\\vvGmbH')
from stockClass import StockAccount, Stock
from datetime import datetime
import pandas as pd

def test_initial_balance():
    account = StockAccount(1000, datetime(2023, 1, 1))
    assert account.get_balance() == 1000

def test_deposit():
    account = StockAccount(1000, datetime(2023, 1, 1))
    account.deposit(100, datetime(2023, 1, 2))
    assert account.get_balance() == 1100

def test_withdraw():
    account = StockAccount(1000, datetime(2023, 1, 1))
    account.withdraw(100, datetime(2023, 1, 2))
    assert account.get_balance() == 900

def test_add_interest():
    account = StockAccount(1000, datetime(2023, 1, 1))
    account.add_interest(datetime(2023, 1, 31))
    assert account.get_balance() == 1020

def test_balance_after_buying_stock():
    account = StockAccount(1000, datetime(2023, 1, 1))
    stock = Stock(100, "Stock A")
    purchase_date = datetime(2023, 1, 15)
    purchase_amount = 100
    purchase_price = 100
    expected_balance = 1000 - purchase_amount
    account.buy_stocks(stock, purchase_amount, purchase_price, purchase_date)
    assert account.get_balance() == expected_balance

def test_buy_stocks():
    account = StockAccount(1000, datetime(2023, 1, 1))
    stock = Stock(100, "Stock A")
    purchase_date = datetime(2023, 1, 15)
    purchase_amount = 50
    purchase_price = 100

    account.buy_stocks(stock, purchase_amount, purchase_price, purchase_date)

    assert account.get_balance() == 950
    assert len(account.stocks) == 1

    transaction = account.stocks.iloc[0]
    assert transaction['stock'] == stock
    assert transaction['date'] == purchase_date
    assert transaction['share_price_at_purchase'] == purchase_price
    assert transaction['number_of_shares'] ==  purchase_amount/purchase_price
    assert transaction['transaction_type'] == 'buy_stock'
    assert transaction['transaction_value'] == purchase_amount

from datetime import datetime
from stockClass import Stock, StockAccount

def test_sell_stocks_with_enough_shares():
    # Create a stock and a stock account with an initial balance
    stock = Stock(100, "Stock A")
    account = StockAccount(1000, datetime(2023, 1, 1))

    # Buy 20 shares of the stock
    account.buy_stocks(stock, 20 * stock.share_price, stock.share_price, datetime(2023, 1, 15))

    # Sell 10 shares
    account.sell_stocks(stock, 10 * stock.share_price, stock.share_price, datetime(2023, 1, 30))

    # Check if the balance is updated correctly
    assert account.get_balance() == 1100

    # Check if the number of shares is updated correctly
    assert account.stocks.iloc[0]['number_of_shares'] == 10


def test_sell_stocks_with_insufficient_shares():
    # Create a stock and a stock account with an initial balance
    stock = Stock(100, "Stock A")
    account = StockAccount(1000, datetime(2023, 1, 1))

    # Buy 20 shares of the stock
    account.buy_stocks(stock, 20 * stock.share_price, stock.share_price, datetime(2023, 1, 15))

    # Sell 30 shares
    account.sell_stocks(stock, 30 * stock.share_price, stock.share_price, datetime(2023, 1, 30))

    # Check if the balance is updated correctly
    assert account.get_balance() == 1000

    # Check if the number of shares is updated correctly
    assert account.stocks.iloc[0]['number_of_shares'] == 0

def test_net_worth():
    account = StockAccount(1000, datetime(2023, 1, 1))
    stock = Stock(100, "Stock A")
    purchase_amount = 10
    purchase_price = 100
    purchase_date = datetime(2023, 1, 15)

    account.add_interest(datetime(2023, 1, 31))
    account.buy_stocks(stock, purchase_amount, purchase_price, purchase_date)

    expected_net_worth = ( 
        account.get_balance() + 
        purchase_amount
    )
    assert account.calculate_net_worth() == expected_net_worth
