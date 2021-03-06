from network import network
from graph import draw
from graph import show
from graph import save
from get_data import get_data
from indicators import CalculateIndicators
import datetime
import time

# Disable UserWarnings on linux promt: export TF_CPP_MIN_LOG_LEVEL=2

## *********************************************************************************
## 1) *** Download data ***

ticker = 'TSLA'
start_date = '20000101'
end_date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d'))

df = get_data(ticker=ticker, start_date=start_date, end_date=end_date)

## *********************************************************************************
## 2) *** Calculat indicators ***

# The first part of the dataset will be cut depending on the indicators parameter to prevent empty data.
ci = CalculateIndicators(df)

# Parameters
ci.set_RSI_parameter(n=14)
ci.set_MACD_parameter(fast=12, slow=26, signal=9)
ci.set_SO_parameter(period=14)
ci.set_moving_average_1(window=12)
ci.set_moving_average_2(window=26)

data = ci.calculate_indicators()

# Normalized Data
data_n = (data - data.mean()) / (data.max() - data.min())

## *********************************************************************************
## 3) *** Set parameters, prepare datasets, testing and training ***

# Parameters
batch_size = 3
test_dataset_size = 0.1  # = 10 percent of the complete dataset for testing
num_units = 12
learning_rate = 0.001
epochs = 10

# All available features:
# ['Close', 'MACD', 'Stochastics', 'ATR', 'RSI', ci.moving_average_1_label, ci.moving_average_2_label]
features = ['MACD', ci.moving_average_1_label]

dataset_train_length = len(data_n.index) - int(len(data_n.index) * test_dataset_size)

predicted_data = network(data_n, features, batch_size, dataset_train_length, num_units, learning_rate, epochs)

## *********************************************************************************
## 4) Draw graph

# Parameters
draw_ATR=True
draw_MACD=True
draw_Stochastics=True
draw_RSI=True
draw_moving_average_1 = True
draw_moving_average_2 = False

# I love to play around with colors :)
accent_color = '#c9c9c9'
indicators_color = '#598720'

# The use of normalized data is necessary for plotting the price and moving averages in the same graph.
data['Close'] = data_n['Close']
data[ci.moving_average_1_label] = data_n[ci.moving_average_1_label]
data[ci.moving_average_2_label] = data_n[ci.moving_average_2_label]
# data['ATR'] = data_n['ATR']
# data['MACD'] = data_n['MACD']
# data['Stochastics'] = data_n['Stochastics']
# data['RSI'] = data_n['RSI']

# Draw
draw(ticker, data[dataset_train_length:], predicted_data, ci,
     draw_moving_average_1 = draw_moving_average_1, draw_moving_average_2=draw_moving_average_2,
     draw_ATR=draw_ATR, draw_MACD=draw_MACD, draw_Stochastics=draw_Stochastics, draw_RSI=draw_RSI,
     accent_color=accent_color, indicators_color=indicators_color)

show()
# save('graph.png')
