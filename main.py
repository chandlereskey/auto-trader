# this file is the main file to run the entire application
import datetime
import os

# while True:
#     current_time = datetime.datetime.now() # need to make this simplified to just hour
#
#     if current_time == '9 am':
#
import schedule
import time

from robin_stocks import robinhood as r

from actions import *

username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
login = r.authentication.login(username, password)

# Schedule your functions to be called at specific hours
schedule.every().hour.at("09:00").do(lambda: BUY())
schedule.every().hour.at("10:00").do(lambda: check_price())
schedule.every().hour.at("11:00").do(lambda: check_price())
schedule.every().hour.at("12:00").do(lambda: check_price())
schedule.every().hour.at("13:00").do(lambda: check_price())
schedule.every().hour.at("14:00").do(lambda: check_price())
schedule.every().hour.at("15:00").do(lambda: check_price())
schedule.every().hour.at("16:00").do(lambda: check_price())
schedule.every().hour.at("16:55").do(lambda: SELL())
schedule.every().hour.at("00:00").do(lambda: retrain_model_and_get_next_day_stock())

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

