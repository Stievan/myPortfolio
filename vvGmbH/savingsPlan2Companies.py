from stockClass import StockAccount, Stock, Visualization
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt

# Initialize a StockAccount with an initial balance of 1000
savings_plan = StockAccount(2500, datetime(2020, 1, 1))

# Create stock objects representing two fictitious companies with different base share prices
company_a = Stock(100, "Company A")
company_b = Stock(100, "Company B")


# Set the initial date to January 1, 2020, at 13:00
current_date = datetime(2020, 1, 1, 13, 0)

# Randomize the stock prices for company A and B within ±30% of their base prices and buy stocks
for company, base_amount in [(company_a, 100), (company_b, 100)]:
    fluctuation = random.uniform(-0.1, 0.1)
    new_price = company.get_value() * (1 + fluctuation)
    savings_plan.buy_stocks(company, base_amount, new_price, current_date)

# Perform a series of operations on the savings account over the course of 36 months
for month in range(36):
    print(f"\nMonth {month+1} ({current_date.strftime('%B %Y')}):")

    # Randomize the stock prices for companies A and B and perform operations
    for company, monthly_deposit in [(company_a, 100), (company_b, 100)]:
        fluctuation = random.uniform(-0.3, 0.3)
        new_price = company.get_value() * (1 + fluctuation)
        company.share_price = new_price
        print(f"Today's share price for company {company.name}: {new_price}")

        # Deposit money into the account every month
        savings_plan.deposit(monthly_deposit, current_date)
        print(f"Deposited {monthly_deposit}, new balance: {savings_plan.get_balance()}")

        # Buy shares of the company every month (using the new random price)
        savings_plan.buy_stocks(company, monthly_deposit, new_price, current_date)
        print(f"Bought shares of company {company.name} worth {monthly_deposit}, new balance: {savings_plan.get_balance()}")

    # Print a monthly overview of the portfolio
    #savings_plan.print_portfolio()

    # Simulate the passage of one month
    current_date += timedelta(days=30)

# Print the transaction history for companies A and B at the end of the period
if 0 :
    for company in [company_a, company_b]:
        print(f"\nTransaction history for company {company.name}:")
        savings_plan.print_stock_transactions(company)

# Create an instance of the Visualization class and generate data for visualization
visualization = Visualization()
visualization.generate_data(savings_plan)

# Plot the recorded data at the end of the script in a single figure with 4 subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 15))

# Plot share prices
for stock, prices in visualization.share_prices.items():
    axs[0].plot(visualization.time_stamps, prices, marker='o', label=str(stock))
axs[0].set_title('Share Price Over Time')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Share Price')
axs[0].grid(True)
axs[0].legend()

# Plot stock values
for stock, values in visualization.stock_values.items():
    axs[1].plot(visualization.time_stamps, values, marker='o', label=str(stock))
axs[1].set_title('Stock Value Over Time')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Stock Value')
axs[1].grid(True)
axs[1].legend()

# Plot portfolio values
axs[2].plot(visualization.time_stamps, visualization.portfolio_values, marker='o', color='green')
axs[2].set_title('Portfolio Value Over Time')
axs[2].set_xlabel('Time')
axs[2].set_ylabel('Portfolio Value')
axs[2].grid(True)

# Plot balances
axs[3].plot(visualization.time_stamps, visualization.balances, marker='o', color='red')
axs[3].set_title('Balance Over Time')
axs[3].set_xlabel('Time')
axs[3].set_ylabel('Balance')
axs[3].grid(True)

plt.tight_layout()
plt.show()
