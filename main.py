# this file is the main file to run the entire application
import datetime

# while True:
#     current_time = datetime.datetime.now() # need to make this simplified to just hour
#
#     if current_time == '9 am':
#
import schedule
import time

value = ''
def job1(test):
    print('testing:', test)

# Schedule your functions to be called at specific hours
schedule.every().hour.at(":33").do(lambda: job1(value))
#schedule.every().hour.at(":00").do(job2)

# Keep the script running
while True:
    value = 'hello'
    schedule.run_pending()
    time.sleep(1)

