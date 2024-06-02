from robin_stocks import robinhood as r
from lstm_model import retrain_and_predict
class Trader:
    def __init__(self):
        # set default to buy NVDA each day
        self.ticker = 'NVDA'
        self.predicted_increase = 1.01
        self.money_spent = 11.08
        self.end_amount = 0.0
    
    def BUY(self):
        if self.ticker:
            equity = float(r.profiles.load_portfolio_profile()['equity'])
            print('BUYING', equity, 'of', self.ticker)
            # buy stock
            buying = r.orders.order_buy_fractional_by_price(symbol=self.ticker, amountInDollars=equity)
            self.money_spent = equity
    
    
    def SELL(self):
        if self.ticker:
            self.end_amount = float(r.profiles.load_portfolio_profile()['market_value'])
            print('SELLING', self.end_amount, 'of', self.ticker)
            selling = r.orders.order_sell_fractional_by_price(symbol=self.ticker, amountInDollars=self.end_amount)
        self.ticker = None
    
    """
    This method trains the model on hostoric data
    then makes a prediction and gets the predicted
    percent gain for the following day's closing price.
    
    It runs for each stock in stocks then sets self.ticker 
    and the predicted increase values.
    """
    def retrain_model_and_get_next_day_stock(self):
        stocks = {'AAPL': 0, 'MSFT': 0, 'NVDA': 0, 'NBIX': 0, 'DXCM': 0}
        for stock in stocks.keys():
            stocks[stock] = retrain_and_predict(stock)
        self.ticker = max(stocks, key=stocks.get)
        self.predicted_increase = stocks[self.ticker]
        if self.predicted_increase and self.predicted_increase < 1.0:
            self.ticker = None
            self.predicted_increase = None
        print(stocks, self.ticker, self.predicted_increase)
    
    """
    This method makes an API call to get the 
    current market value of the account. 
    If the price has reached a threshold then will 
    call the SELL function.
    """
    def check_price(self):
        current_money = float(r.profiles.load_portfolio_profile()['market_value'])
        print('checking price: ', current_money, 'current % increase: ', current_money/self.money_spent)
        if self.predicted_increase and current_money/self.money_spent >= self.predicted_increase:
            self.SELL()
    
    
    """
    This method saves the daily results into a file 
    at the end of the day.
    """
    def daily_results(self):
        print('Start cost: ', self.money_spent, 'ending amount: ', self.end_amount, 'money gained: ', self.end_amount - self.money_spent)
