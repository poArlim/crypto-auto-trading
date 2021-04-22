import pyupbit
import pandas as pd
import numpy as np
import time

# drr = Daily Rate Of Return
# crr = Cumulative Rate Of Return
# mdd = Max Draw Down

coin = "KRW-BTC"
interval = "day"
fees = 0.0005
day_count = 1305

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
df['targetPrice'] = df['open'] + df['range'].shift(1) * 0.28
df['drr'] = np.where(df['high'] > df['targetPrice'], (df['open'].shift(-1) / (1 + fees)) / (df['targetPrice'] * (1 + fees)) - 1, 0)

df['crr'] = 1.0
df['mdd'] = 0.0
df['max_crr'] = 1.0
for i in range(2, day_count) :
    df['crr'][i] = df['crr'][i-1] * (1 + df['drr'][i])
    df['max_crr'][i] = max(df['max_crr'][i-1], df['crr'][i])
    df['mdd'][i] = (df['crr'][i] / df['max_crr'][i]) - 1

print("기간수익률 :", df['crr'][-1] * 100 - 100, "% , 최대손실률 :", min(df['mdd']) * 100, "% , 수수료 :", fees * 100, "%")
print("알고리즘 적용 없을 시 수익률 :", ((df['close'][-1]/(1+fees))/(df['open'][0]*(1+fees))-1) * 100,"%")
df.to_excel("btc_history.xlsx")