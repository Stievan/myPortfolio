from stockClass import BankAccount, Portfolio, Stock, StockTransaction, Visualization
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt

# Initialize a BankAccount with an initial balance of 1000
bank_account = BankAccount(1000, datetime(2020, 1, 1))

# Create a Portfolio linked to the bank account
savings_plan = Portfolio(bank_account)

# Create a stock object representing a fictitious company with a base share price of 100
company_a = Stock(100, "Company A")

# Set the initial date to January 1, 2020, at 13:00
current_date = datetime(2020, 1, 1, 13, 0)

# Randomize the stock price for company A within ±30% of the base price
fluctuation = random.uniform(-0.3, 0.3)
new_price = company_a.get_value() * (1 + fluctuation)

# Buy stocks of company A using the Portfolio's method
savings_plan.buy_stock(company_a, 7, new_price, current_date)

# Perform a series of operations on the portfolio over the course of several months (e.g., for 3 years or 36 months)
for month in range(36):
    print(f"\nMonth {month+1} ({current_date.strftime('%B %Y')}):")

    # Randomize the stock price for company A within ±30% of the base price
    fluctuation = random.uniform(-0.3, 0.3)
    new_price = company_a.get_value() * (1 + fluctuation)
    company_a.update_price(new_price, current_date)
    print(f"Today's share price for company A: {new_price}")

    # Deposit 100 into the bank account every month
    bank_account.deposit(100, current_date)
    print(f"Deposited 100, new balance: {bank_account.get_balance()}")

    # Buy shares of company A every month (using the new random price)
    savings_plan.buy_stock(company_a, 100, new_price, current_date)
    print(f"Bought shares of company A worth 100, new balance: {bank_account.get_balance()}")

    # Simulate the passage of one month
    current_date += timedelta(days=30)

# Now, we will extract the data from the portfolio and stock classes for visualization
dates = savings_plan.value_of_shares.index.tolist()
stock_values = savings_plan.value_of_shares['value_of_shares'].tolist()
portfolio_values = savings_plan.value_of_shares['portfolio_value'].tolist()

# Now, we can plot these values using matplotlib
plt.figure(figsize=(10,6))

# Plot stock values
plt.subplot(3, 1, 1)
plt.plot(dates, stock_values, label='Value of Company A Shares')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

# Plot portfolio values
plt.subplot(3, 1, 2)
plt.plot(dates, portfolio_values, label='Portfolio Value', color='orange')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid(True)

# Plot stock prices
plt.subplot(3, 1, 3)
plt.plot(company_a.price_history['date'], company_a.price_history['price'], label='Company A Stock Price', color='green')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
