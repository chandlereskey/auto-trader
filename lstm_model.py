import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
#import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from datetime import datetime, timedelta

# CREDIT
# This code is pretty much a direct copy of https://github.com/teobeeguan/Python-For-Finance/blob/main/Predict%20Stock%20Price%20Using%20LSTM/stock_price_lstm.ipynb

def retrain_and_predict(ticker):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    stock_data = yf.download(ticker, start='2016-01-01', end=tomorrow)
    stock_data.head()

    # plt.figure(figsize=(15, 8))
    # plt.title('Stock Prices History')
    # plt.plot(stock_data['Close'])
    # plt.xlabel('Date')
    # plt.ylabel('Prices ($)')

    close_prices = stock_data['Close']
    values = close_prices.values
    training_data_len = math.ceil(len(values) - 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(values.reshape(-1, 1))

    train_data = scaled_data[0: training_data_len, :]

    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    test_data = scaled_data[training_data_len - 60:, :]
    x_test = []
    y_test = values[training_data_len:]

    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    model = keras.Sequential()
    model.add(layers.LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(layers.LSTM(100, return_sequences=False))
    model.add(layers.Dense(25))
    model.add(layers.Dense(1))
    model.summary()

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=1, epochs=3)

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
    rmse

    data = stock_data.filter(['Close'])
    train = data[:training_data_len]
    validation = data[training_data_len:]
    validation['Predictions'] = predictions
    # plt.figure(figsize=(16,8))
    # plt.title('Model')
    # plt.xlabel('Date')
    # plt.ylabel('Close Price USD ($)')
    # plt.plot(train)
    # plt.plot(validation[['Close', 'Predictions']])
    # plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    # plt.show()

    prev_close = stock_data['Close'][-2]  # close of previous day
    predicted_next_day_close = validation['Predictions'][0]  # prediction for day
    predicted_percent_increase = predicted_next_day_close / prev_close
    print(validation['Predictions'])
    return float(predicted_percent_increase)
