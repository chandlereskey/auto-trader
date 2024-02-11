"""
This method takes a stock ticker and the
current amount of money available in robinhood

@param ticker: ticker string
@param available_money: integer value of money
@return number of stocks bought
"""
def BUY(ticker: str, available_money: int):
    pass


"""
This method takes the ticker value for the day. 
It returns the time 
sold and the amount of money in the account.

@param ticker: this is stock ticker value for the day
@return returns the time sold and the amount sold for 
        (or money in the account)
"""
def SELL(ticker: str):
    pass


"""
This method retrains the model based on the 
current day's results.
"""
def retrain_model():
    pass


"""
This method runs the model and gets the results 
being the stock ticker chosen along with the prediction.

@return ticker and predicted percent increase
"""
def choose_stock():
    pass


"""
This method makes an API call for the ticker
passed in. 

@param ticker: this is stock ticker value for the day
@return current price
"""
def check_price(ticker: str):
    pass


"""
This method saves the daily results into a file 
at the end of the day.
"""
def daily_results():
    pass
