import os
import schedule
import time

from robin_stocks import robinhood as r

from actions import *

username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
login = r.authentication.login(username, password)

# Schedule your functions to be called at specific hours
schedule.every().day.at("09:30").do(lambda: BUY())
schedule.every().day.at("10:00").do(lambda: check_price())
schedule.every().day.at("10:30").do(lambda: check_price())
schedule.every().day.at("11:00").do(lambda: check_price())
schedule.every().day.at("11:30").do(lambda: check_price())
schedule.every().day.at("12:00").do(lambda: check_price())
schedule.every().day.at("12:30").do(lambda: check_price())
schedule.every().day.at("13:00").do(lambda: check_price())
schedule.every().day.at("13:30").do(lambda: check_price())
schedule.every().day.at("14:00").do(lambda: check_price())
schedule.every().day.at("14:30").do(lambda: check_price())
schedule.every().day.at("15:00").do(lambda: check_price())
schedule.every().day.at("15:30").do(lambda: check_price())
schedule.every().day.at("15:55").do(lambda: SELL())
schedule.every().day.at("08:45").do(lambda: retrain_model_and_get_next_day_stock())

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

