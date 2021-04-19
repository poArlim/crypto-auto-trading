import pyupbit
import pandas as pd
import time

coin = "KRW-BTC"
interval = "day"
fees = 0.0005
day_count = 1000

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
df.to_excel("btc_history.xlsx")