import pyupbit
import pandas as pd
import numpy as np
import time

# drr = Daily Rate Of Return
# crr = Cumulative Rate Of Return
# mdd = Max Draw Down, dd = Draw Down

def get_crr(df, fees, K) :
    df['range'] = df['high'].shift(1) - df['low'].shift(1)
    df['targetPrice'] = df['open'] + df['range'] * K
    df['drr'] = np.where(df['high'] > df['targetPrice'], (df['close'] / (1 + fees)) / (df['targetPrice'] * (1 + fees)) , 1)
    return df['drr'].cumprod()[-2]

def get_best_K(coin, fees, to) :
    df = pyupbit.get_ohlcv(coin, to = to, interval = "day", count = 21)
    time.sleep(0.1)
    max_crr = 0
    best_K = 0.5
    for k in np.arange(0.0, 1.0, 0.1) :
        crr = get_crr(df, fees, k)
        if crr > max_crr :
            max_crr = crr
            best_K = k
    return best_K

coin = "KRW-BTC"
interval = "day"
fees = 0.0005
day_count = 1300
K = 0.5

date = None
dfs = [ ]

for i in range(day_count // 200 + 1):
    if i < day_count // 200 :
        df = pyupbit.get_ohlcv(coin, to = date, interval = interval)
        date = df.index[0]
    elif day_count % 200 != 0 :
        df = pyupbit.get_ohlcv(coin, to = date, interval = interval, count = day_count % 200)
    else :
        break
    dfs.append(df)
    time.sleep(0.1)

df = pd.concat(dfs).sort_index()

df['range'] = df['high'].shift(1) - df['low'].shift(1)
df['best_K'] = 0.5
for i in range(1, day_count) :
    print(i)
    df['best_K'][i] = get_best_K(coin, fees, df.index[i])
df['targetPrice'] = df['open'] + df['range'] * df['best_K']
df['drr'] = np.where(df['high'] > df['targetPrice'], (df['close'] / (1 + fees)) / (df['targetPrice'] * (1 + fees)) - 1 , 0)

df['crr'] = (df['drr'] + 1).cumprod() - 1
df['dd'] = -(((df['crr'] + 1).cummax() - (df['crr'] + 1)) / (df['crr'] + 1).cummax())

print("기간수익률 :", df['crr'][-1] * 100, "% , 최대손실률 :", df['dd'].min() * 100, "% , 수수료 :", fees * 100, "%")
print("알고리즘 적용 없을 시 수익률 :", ((df['close'][-1]/(1+fees))/(df['open'][0]*(1+fees))-1) * 100,"%")

df.to_excel("crypto_history.xlsx")