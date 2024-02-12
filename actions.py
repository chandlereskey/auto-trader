from robin_stocks import robinhood as r
from lstm_model import retrain_and_predict

# set up global variables
ticker = 'AAPL'
predicted_increase = 1.01
money_spent = 11
end_amount = 0

"""
    This method takes a stock ticker and the
    current amount of money available in robinhood
    
    @param ticker: ticker string
    @param available_money: integer value of money
    @return number of stocks bought
"""
def BUY():
    global ticker, money_spent
    if ticker:
        equity = float(r.profiles.load_portfolio_profile()['equity'])
        print('BUYING', equity, 'of', ticker)
        # buy stock
        buying = r.orders.order_buy_fractional_by_price(symbol=ticker, amountInDollars=equity)
        money_spent = equity


"""
This method takes the ticker value for the day. 
It returns the time 
sold and the amount of money in the account.

@param ticker: this is stock ticker value for the day
@return returns the time sold and the amount sold for 
        (or money in the account)
"""
def SELL():
    global ticker, end_amount
    if ticker:
        end_amount = float(r.profiles.load_portfolio_profile()['market_value'])
        print('SELLING', end_amount, 'of', ticker)
        selling = r.orders.order_sell_fractional_by_price(symbol=ticker, amountInDollars=end_amount)
    ticker = None

"""
This method retrains the model based on the 
current day's results and reruns the model to get
following day prediction.

This will run the model on each stock ticker and get the
predicted percent increase

It will set the value of the ticker
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
This method makes an API call for the ticker
passed in. If the price has reached a threshold then will 
call the SELL function.

@param ticker: this is stock ticker value for the day
@return current price
"""
def check_price():
    global predicted_increase, money_spent
    current_money = float(r.profiles.load_portfolio_profile()['market_value'])
    print('checking price: ', current_money)
    if predicted_increase and current_money/money_spent >= predicted_increase:
        SELL()


"""
This method saves the daily results into a file 
at the end of the day.
"""
def daily_results():
    global money_spent, end_amount
    print('Start cost: ', money_spent, 'ending amount: ', end_amount)
