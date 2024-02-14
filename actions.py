from robin_stocks import robinhood as r
from lstm_model import retrain_and_predict

# set up global variables
ticker = None
predicted_increase = 0.0
money_spent = 0.0
end_amount = 0.0

def BUY():
    global ticker, money_spent
    if ticker:
        equity = float(r.profiles.load_portfolio_profile()['equity'])
        print('BUYING', equity, 'of', ticker)
        # buy stock
        buying = r.orders.order_buy_fractional_by_price(symbol=ticker, amountInDollars=equity)
        money_spent = equity


def SELL():
    global ticker, end_amount
    if ticker:
        end_amount = float(r.profiles.load_portfolio_profile()['market_value'])
        print('SELLING', end_amount, 'of', ticker)
        selling = r.orders.order_sell_fractional_by_price(symbol=ticker, amountInDollars=end_amount)
    ticker = None

"""
This method trains the model on hostoric data
then makes a prediction and gets the predicted
percent gain for the following day's closing price.

It runs for each stock in stocks then sets ticker 
and the predicted increase values.
"""
def retrain_model_and_get_next_day_stock():
    global ticker, predicted_increase
    stocks = {'AAPL': 0, 'MSFT': 0, 'NVDA': 0, 'NBIX': 0, 'DXCM': 0}
    for stock in stocks.keys():
        stocks[stock] = retrain_and_predict(stock)
    ticker = max(stocks, key=stocks.get)
    predicted_increase = stocks[ticker]
    if predicted_increase and predicted_increase < 1.0:
        ticker = None
        predicted_increase = None
    print(stocks, ticker, predicted_increase)

"""
This method makes an API call to get the 
current market value of the account. 
If the price has reached a threshold then will 
call the SELL function.
"""
def check_price():
    global predicted_increase, money_spent
    current_money = float(r.profiles.load_portfolio_profile()['market_value'])
    print('checking price: ', current_money, 'current % increase: ', current_money/money_spent)
    if predicted_increase and current_money/money_spent >= predicted_increase:
        SELL()


"""
This method saves the daily results into a file 
at the end of the day.
"""
def daily_results():
    global money_spent, end_amount
    print('Start cost: ', money_spent, 'ending amount: ', end_amount, 'money gained: ', end_amount - money_spent)
