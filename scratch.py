import os

from robin_stocks import robinhood as r
username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
login = r.authentication.login(username, password)

ticker = 'AAPL'
if ticker:
    end_amount = float(r.profiles.load_portfolio_profile()['market_value'])
    print('SELLING', end_amount, 'of', ticker)
    selling = r.orders.order_sell_fractional_by_price(symbol=ticker, amountInDollars=end_amount)
ticker = None