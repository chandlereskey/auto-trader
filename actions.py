from robin_stocks import robinhood as r
from lstm_model import retrain_and_predict

# set up global variables
ticker = None
predicted_increase = None
money_spent = 0
end_amount = 0

"""
    This method takes a stock ticker and the
    current amount of money available in robinhood
    
    @param ticker: ticker string
    @param available_money: integer value of money
    @return number of stocks bought
"""
def BUY():
    if ticker:
        equity = r.profiles.load_portfolio_profile()['equity']
        # buy stock
        global money_spent
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
    if ticker:
        global end_amount
        end_amount = r.profiles.load_portfolio_profile()['market_value']
        r.orders.order_sell_fractional_by_price(symbol=ticker, amountInDollars=end_amount)
    global ticker
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
    stocks = {'AAPL': 0, 'MSFT': 0, 'NVDA': 0, 'NBIX': 0, 'DXCM': 0}
    for stock in stocks.keys():
        stocks[stock] = retrain_and_predict(stock)
    global ticker
    global predicted_increase
    ticker = max(stocks, key=stocks.get)
    predicted_increase = stocks[ticker]
    if predicted_increase < 1:
        ticker = None
        predicted_increase = None

"""
This method makes an API call for the ticker
passed in. If the price has reached a threshold then will 
call the SELL function.

@param ticker: this is stock ticker value for the day
@return current price
"""
def check_price():
    current_money = r.profiles.load_portfolio_profile()['market_value']
    if current_money/money_spent >= predicted_increase:
        SELL()


"""
This method saves the daily results into a file 
at the end of the day.
"""
def daily_results():
    print('Start cost: ', money_spent, 'ending amount: ', end_amount)
