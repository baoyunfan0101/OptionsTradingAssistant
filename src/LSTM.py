import pandas as pd
from numpy import array
import json
import requests

import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout

import os
import pickle

# 设置参数
n_timestamp = 50  # 时间戳
n_epochs = 100  # 迭代次数

# code_list
code_list = ['510050', '510300', '510500', '159901', '159915', '159919', '159922']

# code - exchange
dict = {'510050': 'sh',
        '510300': 'sh',
        '510500': 'sh',
        '159901': 'sz',
        '159915': 'sz',
        '159919': 'sz',
        '159922': 'sz',
        }

# 设置中文字体为宋体
plt.rcParams['font.sans-serif'] = ['SimSun']

# 不显示警告信息
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# exchange - 交易所('sh', 'sz'); code - 股票代码; datalen - 数据长度
def get_k_line(exchange, code, datalen):
    symbol = exchange + code
    r = requests.get(
        'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=' + symbol + '&scale=60&ma=no&datalen=' + datalen)
    data = pd.DataFrame(json.loads(r.text))
    return data


# 取前(n_timestamp)天的数据为X, 第(n_timestamp+1)天数据为Y
def data_split(sequence, n_timestamp):
    X = []
    Y = []
    for i in range(len(sequence)):
        end_ix = i + n_timestamp

        if end_ix > len(sequence) - 1:
            break

        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        Y.append(seq_y)
    return array(X), array(Y)


# 建立并训练LSTM模型
def myLSTM(X_train, Y_train, X_test, Y_test):
    tf.config.list_physical_devices('CPU')

    # 建立双层LSTM
    model = Sequential()
    model.add(LSTM(units=32, activation='tanh', return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(units=64, activation='tanh'))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dropout(rate=0.2))
    model.add(Dense(units=1, activation='relu'))
    model.compile(loss='mean_squared_error', optimizer='Adam')

    # 训练LSTM
    history = model.fit(X_train, Y_train,
                        batch_size=64,
                        epochs=n_epochs,
                        validation_data=(X_test, Y_test),
                        validation_freq=1)

    model.summary()

    # 损失函数
    plt.plot(history.history['loss'], label='训练损失')
    plt.plot(history.history['val_loss'], linestyle='--', label='验证损失')
    plt.xlabel('迭代次数')
    plt.ylabel('损失值')
    plt.legend()
    plt.show()

    return model


# 预测
def predict(X_test, Y_test, model, sc):
    predicted_stock_price = model.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)  # 反归一化
    real_stock_price = sc.inverse_transform(Y_test)

    # 真实数据和预测数据的对比曲线
    plt.plot(real_stock_price, color='red', label='实际股票价格')
    plt.plot(predicted_stock_price, color='blue', linestyle='--', label='预测股票价格')
    plt.xlabel('时间')
    plt.ylabel('价格')
    plt.legend()
    plt.show()

    # 评价指标
    MSE = metrics.mean_squared_error(predicted_stock_price, real_stock_price)
    RMSE = metrics.mean_squared_error(predicted_stock_price, real_stock_price) ** 0.5
    MAE = metrics.mean_absolute_error(predicted_stock_price, real_stock_price)
    R2 = metrics.r2_score(predicted_stock_price, real_stock_price)

    print('均方误差: %.5f' % MSE)
    print('均方根误差: %.5f' % RMSE)
    print('平均绝对误差: %.5f' % MAE)
    print('R2: %.5f' % R2)

    return real_stock_price


# 获取LSTM模型
def train_LSTM(ex, code, datalen='1023', ifsave=True):
    data = get_k_line(ex, code, datalen)

    # 划分训练集、测试集
    training_set = data.iloc[0:len(data) - 300, 4:5]
    test_set = data.iloc[len(data) - 300:, 4:5]

    # 归一标准化
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    testing_set_scaled = sc.transform(test_set)

    # 划分X、Y
    X_train, Y_train = data_split(training_set_scaled, n_timestamp)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

    X_test, Y_test = data_split(testing_set_scaled, n_timestamp)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # 训练
    model = myLSTM(X_train, Y_train, X_test, Y_test)

    # 预测
    predict(X_test, Y_test, model, sc)

    # 保存模型
    if ifsave:
        model.save(code + '.h5')
        with open(code + '_sc.pkl', 'wb') as f:
            pickle.dump(sc, f)


# 计算价值潜力
def get_VP(code, delta, proportion=1):
    if os.path.exists(code + '.h5'):
        model = load_model(code + '.h5')
        with open(code + '_sc.pkl', 'rb') as f:
            sc = pickle.load(f)

    data = get_k_line(dict[code], code, '50')

    X_test = data.iloc[:, 4:5]
    X_test_scaled = sc.transform(X_test)
    X_test_scaled = array([X_test_scaled])
    X_test_scaled = X_test_scaled.reshape(X_test_scaled.shape[0], X_test_scaled.shape[1], 1)

    predicted = model.predict(X_test_scaled)
    predicted = sc.inverse_transform(predicted)  # 反归一化

    return delta * proportion * (predicted[0][0] - float(X_test.iat[-1, 0]))


# 重新训练所有LSTM模型
def train_all_models():
    for code in code_list:
        train_LSTM(dict[code], code, '1023', True)


# 计算所有价值潜力
def get_all_VPs():
    res = {}

    for code in code_list:
        if os.path.exists(code + '.h5'):
            model = load_model(code + '.h5')
            with open(code + '_sc.pkl', 'rb') as f:
                sc = pickle.load(f)

        data = get_k_line(dict[code], code, '50')

        X_test = data.iloc[:, 4:5]
        X_test_scaled = sc.transform(X_test)
        X_test_scaled = array([X_test_scaled])
        X_test_scaled = X_test_scaled.reshape(X_test_scaled.shape[0], X_test_scaled.shape[1], 1)

        predicted = model.predict(X_test_scaled)
        predicted = sc.inverse_transform(predicted)  # 反归一化

        res[code] = predicted[0][0] - float(X_test.iat[-1, 0])

    return res


if __name__ == '__main__':
    # train_LSTM('sh', '510050', '1023', False)
    # train_LSTM('sh', '510300', '1023', False)
    # train_LSTM('sh', '510500', '1023', False)
    # train_LSTM('sz', '159901', '1023', False)
    # train_LSTM('sz', '159915', '1023', False)
    # train_LSTM('sz', '159919', '1023', False)
    # train_LSTM('sz', '159922', '1023', False)
    train_all_models()
    pass
