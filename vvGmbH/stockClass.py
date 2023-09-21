

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from uuid import uuid4
from uuid import UUID

class Stock:
    def __init__(self, initial_price, name):
        self.id = uuid4()  # Generating a unique ID for the stock instance
        self.name = name
        self.current_price = initial_price
        self.price_history = pd.DataFrame(columns=['date', 'price'])  # Dataframe to store the history of price changes

    def update_price(self, new_price, date):
        """
        Updates the stock's price and records the change in the price history.

        :param new_price: The new price of the stock.
        :param date: The date of the price change.
        """
        new_data = pd.DataFrame([{'date': date, 'price': new_price}])
        self.price_history = pd.concat([self.price_history, new_data], ignore_index=True)
        self.current_price = new_price


    def import_price_history(self, df):
        """
        Imports a history of price changes from a dataframe.

        :param df: A pandas DataFrame with columns 'date' and 'price' representing the price history.
        """
        if 'date' in df.columns and 'price' in df.columns:
            self.price_history = pd.concat([self.price_history, df], ignore_index=True)
        else:
            print("Error: The dataframe must contain 'date' and 'price' columns.")

    def get_price_on_date(self, date):
        """
        Gets the stock's price on a specific date.

        :param date: The date to query the price.
        :return: The price on the specified date or a message indicating that the price data for the date is not available.
        """
        price_data = self.price_history[self.price_history['date'] == date]
        if not price_data.empty:
            return price_data.iloc[0]['price']
        else:
            return f"Error: No price data available for the date {date}."

    def get_value(self):
        """
        Gets the current value of the stock.

        :return: The current price of the stock.
        """
        return self.current_price
    
    def get_last_known_price(self):
        """
        Gets the last known price of the stock.

        :return: The last known price of the stock, or None if the price history is empty.
        """
        if not self.price_history.empty:
            return self.price_history.iloc[-1]['price']
        else:
            return None

    def get_price_history(self):
        """
        Gets the history of price changes for the stock.

        :return: A dataframe representing the price history.
        """
        return self.price_history

    def __str__(self):
        return f"Stock(ID: {self.id}, Name: {self.name}, Current Price: {self.current_price})"



class StockTransaction:
    def __init__(self, stock, date, transaction_type, number_of_shares, share_price_at_purchase):
        self.id = uuid4()  # Generating a unique ID for the transaction
        self.stock = stock
        self.date = date
        self.transaction_type = transaction_type
        self.number_of_shares = number_of_shares
        self.share_price_at_purchase = share_price_at_purchase

    def get_transaction_value(self):
        """
        Calculates the transaction value.

        :return: The total value of the transaction.
        """
        return self.number_of_shares * self.share_price_at_purchase

    def __str__(self):
        return f"StockTransaction(ID: {self.id}, Stock ID: {self.stock.id}, Type: {self.transaction_type}, Number of Shares: {self.number_of_shares}, Share Price at Purchase: {self.share_price_at_purchase})"



class BankAccount:
    def __init__(self, initial_balance, start_date):
        self.balance = initial_balance
        self.balance_history = pd.DataFrame(columns=['date', 'transaction_type', 'transaction_value', 'balance'])
        self.balance_history = pd.concat([
            self.balance_history, 
            pd.DataFrame([{
                'date': start_date, 
                'transaction_type': 'monetary_flow', 
                'transaction_value': initial_balance, 
                'balance': initial_balance
            }])
        ], ignore_index=True)
        self.interest_rate = 0.02

    def deposit(self, amount, date):
        self.balance += amount
        self._add_balance_history(date, 'monetary_flow', amount)

    def withdraw(self, amount, date):
        self.balance -= amount
        self._add_balance_history(date, 'monetary_flow', -amount)

    def add_interest(self, date):
        interest_value = self.balance * self.interest_rate
        self.balance += interest_value
        self._add_balance_history(date, 'monetary_flow', interest_value)

    def get_balance(self):
        return self.balance

    def _add_balance_history(self, date, transaction_type, transaction_value):
        new_entry = pd.DataFrame([{
            'date': date, 
            'transaction_type': transaction_type, 
            'transaction_value': transaction_value, 
            'balance': self.balance
        }])
        self.balance_history = pd.concat([self.balance_history, new_entry], ignore_index=True)
    
    def get_balance_history(self):
        return self.balance_history

    def __str__(self):
        return f"BankAccount(Balance: {self.balance})"



class Portfolio:
    def __init__(self, bank_account):
        self.bank_account = bank_account
        self.transactions = []  # List to store all stock transactions
        self.stocks = {}  # Dictionary to store the current holdings (key: stock ID, value: dictionary with number of shares and value of shares)
        self.portfolio_value_history = pd.DataFrame(columns=['date', 'value'])  # DataFrame to store portfolio value history


    def buy_stock(self, stock, number_of_shares, price_per_share, date):
        """
        Buys the specified number of shares of a stock at the given price per share on the given date.
        
        :param stock: The stock to buy.
        :param number_of_shares: The number of shares to buy.
        :param price_per_share: The price per share.
        :param date: The date of the transaction.
        """
        # Check if the stock parameter is an instance of the Stock class
        if not isinstance(stock, Stock):
            raise TypeError("stock must be an instance of the Stock class")

        # Calculate the cost of the transaction
        cost = number_of_shares * price_per_share

        # Check if the bank account balance is sufficient
        if self.bank_account.get_balance() >= cost:
            # Withdraw the cost from the bank account
            self.bank_account.withdraw(cost, date)

            # Add the stock to the portfolio (or update the number of shares if already present)
            if stock.id not in self.stocks:
                self.stocks[stock.id] = {"stock_object": stock, "number_of_shares": 0, "history": pd.DataFrame(columns=['date', 'stock_id', 'number_of_shares', 'price_per_share'])}
            self.stocks[stock.id]["number_of_shares"] += number_of_shares

            # Create a new stock transaction and add it to the list of transactions
            self.transactions.append(StockTransaction(stock, date, "BUY", number_of_shares, price_per_share))


            # Update the stock history
            new_history_record = pd.DataFrame({
                'date': [date],
                'stock_id': [stock.id],
                'number_of_shares': [number_of_shares],
                'price_per_share': [price_per_share]
            })
            self.stocks[stock.id]['history'] = pd.concat([self.stocks[stock.id]['history'], new_history_record], ignore_index=True)

            # Update the portfolio value
            self.get_portfolio_value(date)
        else:
            # Raise an error if there are insufficient funds
            raise ValueError("Insufficient funds in bank account")


    def sell_stock(self, stock, number_of_shares, price_per_share, date):
        """
        Sells the specified number of shares of a stock at the given price per share on the given date.
        
        :param stock: The stock to sell.
        :param number_of_shares: The number of shares to sell.
        :param price_per_share: The price per share.
        :param date: The date of the transaction.
        """
        # Check if the stock parameter is an instance of the Stock class
        if not isinstance(stock, Stock):
            raise TypeError("stock must be an instance of the Stock class")

        # Check if the portfolio contains the stock to be sold
        if stock.id not in self.stocks or self.stocks[stock.id]["number_of_shares"] < number_of_shares:
            raise ValueError("Insufficient shares to sell")

        # Calculate the proceeds of the sale
        proceeds = number_of_shares * price_per_share

        # Update the number of shares in the portfolio
        self.stocks[stock.id]["number_of_shares"] -= number_of_shares

        # Deposit the proceeds into the bank account
        self.bank_account.deposit(proceeds, date)

        # Create a new stock transaction and add it to the list of transactions
        self.transactions.append(StockTransaction(stock, -number_of_shares, price_per_share, date))

        # Update the stock history
        new_history_record = pd.DataFrame({
            'date': [date],
            'stock_id': [stock.id],
            'number_of_shares': [-number_of_shares],  # Note the negative sign to indicate sale
            'price_per_share': [price_per_share]
        })
        self.stocks[stock.id]['history'] = pd.concat([self.stocks[stock.id]['history'], new_history_record], ignore_index=True)

        # Update the portfolio value
        self.get_portfolio_value(date)



    def get_stock_transactions(self, stock):
        """
        Method to get all transactions associated with a particular stock.

        :param stock: The Stock object to query transactions for.
        :return: A list of StockTransaction objects associated with the stock.
        """
        return [transaction for transaction in self.transactions if transaction.stock.id == stock.id]

    def calculate_net_worth(self):
        """
        Method to calculate the net worth of the portfolio.

        :return: The net worth calculated as the sum of the balance in the bank account and the current value of the stocks in the portfolio.
        """
        net_worth = self.bank_account.get_balance()
        for stock_id, number_of_shares in self.stocks.items():
            # Assuming a method get_stock_by_id is defined to get a Stock object by its ID
            stock = get_stock_by_id(stock_id)  
            net_worth += stock.get_value() * number_of_shares
        return net_worth
    
    def get_total_shares_owned(self, stock):
        transactions = self.get_stock_transactions(stock)
        total_shares_owned = sum(transaction.number_of_shares for transaction in transactions if transaction.transaction_type == 'buy_stock') - \
                            sum(transaction.number_of_shares for transaction in transactions if transaction.transaction_type == 'sell_stock')
        return total_shares_owned

    def get_portfolio_value(self, date):
        total_value = 0
        for stock_data in self.stocks.values():
            total_value += stock_data['value_of_shares']

        # Update portfolio value history
        new_data = pd.DataFrame([{'date': date, 'value': total_value}])
        self.portfolio_value_history = pd.concat([self.portfolio_value_history, new_data], ignore_index=True)
        
        return total_value


    def print_portfolio(self):
        """
        Method to print the details of the current portfolio including transactions and current holdings.
        """
        # ... (Implementation to print the portfolio details)
        pass


    def get_stock_by_id(self, stock_id):
        # Here, self refers to the Portfolio instance, so you can access its attributes and methods
        return self.stocks.get(stock_id, None)


    def get_portfolio_value(self, date):
        """
        Gets the total value of the portfolio at the specified date.

        :param date: The date at which to get the portfolio value.
        :return: The total value of the portfolio at the date.
        """
        self.update_stock_values(date)
        return sum(self.stock_values.values())

    def get_total_shares_owned(self, stock):
        """
        Gets the total number of shares owned of the specified stock.

        :param stock: The Stock object to query.
        :return: The total number of shares owned of the stock.
        """
        transactions = self.get_stock_transactions(stock)
        total_shares_owned = sum(transaction.number_of_shares for transaction in transactions if transaction.transaction_type == 'buy_stock') - \
                             sum(transaction.number_of_shares for transaction in transactions if transaction.transaction_type == 'sell_stock')
        return total_shares_owned

    def __str__(self):
        return f"Portfolio(Net Worth: {self.calculate_net_worth()})"


class StockManager:
    def __init__(self):
        # Dictionary to store all stock instances keyed by their unique IDs
        self.stocks = {}

    def add_stock(self, stock):
        """
        Adds a stock instance to the manager.

        :param stock: Stock instance to be added.
        """
        self.stocks[stock.id] = stock

    def get_stock_by_id(self, stock_id):
        """
        Retrieves a stock instance by its ID.

        :param stock_id: The UUID of the stock to retrieve.
        :return: The Stock instance if found, or None if not found.
        """
        return self.stocks.get(stock_id)

    def __str__(self):
        return f"StockManager(Stock Count: {len(self.stocks)})"


# Utility function to get a stock instance by its ID
def get_stock_by_id(stock_id: UUID, stock_manager: StockManager):
    """
    Retrieves a stock instance by its ID using a StockManager instance.

    :param stock_id: The UUID of the stock to retrieve.
    :param stock_manager: The StockManager instance managing the stocks.
    :return: The Stock instance if found, or None if not found.
    """
    return stock_manager.get_stock_by_id(stock_id)



class Visualization:
    """A class for visualizing the stock and portfolio data over time."""
    
    def __init__(self) -> None:
        """Initializes a Visualization object with empty data structures to store visualization data."""
        self.time_stamps = []
        self.share_prices = {}  
        self.stock_values = {}  
        self.portfolio_values = []
        self.balances = []  

    def generate_data(self, stock_account: 'StockAccount') -> None:
        """
        Generates data for visualization based on the transaction history of a stock account.

        :param stock_account: The stock account object whose data is to be visualized.
        """
        # Reset data
        self.time_stamps = []
        self.portfolio_values = []
        self.balances = [] 

        # Create dictionaries to store the latest share price and total shares owned for each stock
        latest_share_prices = {}
        total_shares_owned = {}

        # Initialize balance
        balance = stock_account.get_initial_balance()

        # Initialize a set to keep track of stocks that have been encountered
        encountered_stocks = set()
        
        # Iterate through transactions and generate data
        for transaction in sorted(stock_account.stocks + stock_account.balance_history, key=lambda x: x['date']):
            date = transaction['date']
            transaction_type = transaction['transaction_type']
            
            if 'stock' in transaction:
                stock = transaction['stock']
                encountered_stocks.add(stock)
                
                if transaction_type == 'buy_stock':
                    total_shares_owned[stock] = total_shares_owned.get(stock, 0) + transaction['number_of_shares']
                    balance -= transaction['transaction_value']
                elif transaction_type == 'sell_stock':
                    total_shares_owned[stock] = total_shares_owned.get(stock, 0) - transaction['number_of_shares']
                    balance += transaction['transaction_value']
                
                latest_share_prices[stock] = transaction.get('share_price_at_purchase', latest_share_prices.get(stock, 0))

            elif transaction_type == 'monetary_flow':
                balance += transaction['transaction_value']

            # Calculate stock value and portfolio value
            stock_value = sum(latest_share_prices[s] * total_shares_owned[s] for s in latest_share_prices)
            portfolio_value = balance + stock_value

            # Record data
            self.time_stamps.append(date)
            for stock in encountered_stocks:
                if stock not in self.share_prices:
                    self.share_prices[stock] = [0] * (len(self.time_stamps) - 1)
                    self.stock_values[stock] = [0] * (len(self.time_stamps) - 1)

                self.share_prices[stock].append(latest_share_prices.get(stock, 0))
                self.stock_values[stock].append(latest_share_prices.get(stock, 0) * total_shares_owned.get(stock, 0))
            
            self.portfolio_values.append(portfolio_value)
            self.balances.append(balance)

    def plot_data(self) -> None:
        """Plots the visualization data in a single figure with 4 subplots: share prices, stock values, balances, and portfolio values."""
        fig, axs = plt.subplots(4, 1, figsize=(10, 15))

        # Plot share prices
        axs[0].plot(self.time_stamps, [prices for prices in self.share_prices.values()], marker='o')
        axs[0].set_title('Share Prices Over Time')
        axs[0].set_xlabel('Time')
        axs[0].set_ylabel('Share Price')
        axs[0].grid(True)

        # Plot stock values
        axs[1].plot(self.time_stamps, [values for values in self.stock_values.values()], marker='o', color='orange')
        axs[1].set_title('Stock Values Over Time')
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Stock Value')
        axs[1].grid(True)

        # Plot balances
        axs[2].plot(self.time_stamps, self.balances, marker='o', color='green')
        axs[2].set_title('Balances Over Time')
        axs[2].set_xlabel('Time')
        axs[2].set_ylabel('Balance')
        axs[2].grid(True)

        # Plot portfolio values
        axs[3].plot(self.time_stamps, self.portfolio_values, marker='o', color='blue')
        axs[3].set_title('Portfolio Values Over Time')
        axs[3].set_xlabel('Time')
        axs[3].set_ylabel('Portfolio Value')
        axs[3].grid(True)

        plt.tight_layout()
        plt.show()

