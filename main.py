import os
import schedule
import time

from robin_stocks import robinhood as r
from actions import *

# login to robinhood
username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
login = r.authentication.login(username, password)

# Schedule your functions to be called at specific hours each day
t = Trader()
schedule.every().day.at("06:00").do(lambda: t.retrain_model_and_get_next_day_stock())
schedule.every().day.at("09:40").do(lambda: t.BUY())
schedule.every().day.at("10:00").do(lambda: t.check_price())
schedule.every().day.at("10:30").do(lambda: t.check_price())
schedule.every().day.at("11:00").do(lambda: t.check_price())
schedule.every().day.at("11:30").do(lambda: t.check_price())
schedule.every().day.at("12:00").do(lambda: t.check_price())
schedule.every().day.at("12:30").do(lambda: t.check_price())
schedule.every().day.at("13:00").do(lambda: t.check_price())
schedule.every().day.at("13:30").do(lambda: t.check_price())
schedule.every().day.at("14:00").do(lambda: t.check_price())
schedule.every().day.at("14:30").do(lambda: t.check_price())
schedule.every().day.at("15:00").do(lambda: t.check_price())
schedule.every().day.at("15:30").do(lambda: t.check_price())
schedule.every().day.at("15:58").do(lambda: t.SELL())

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

