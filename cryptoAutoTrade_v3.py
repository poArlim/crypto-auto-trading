import pyupbit
import datetime
import time, calendar
import auth             # save 'access key' and 'secret key'
import numpy as np
import requests

def post_message(text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+auth.myToken},
        data={"channel": auth.channel,"text": text}
    )
    #print(response)

def get_targetPrice(df, K) :
    range = df['high'][-2] - df['low'][-2]
    return df['open'][-1] + range * K

def buy_all(coin) :
    balance = upbit.get_balance("KRW") * 0.9995
    if balance >= 5000 :
        buy_result = upbit.buy_market_order(coin, balance)
        print(buy_result)
        post_message("매수 체결.\n체결 단가 : "+str(buy_result['price']))

def sell_all(coin) :
    balance = upbit.get_balance(coin)
    price = pyupbit.get_current_price(coin)
    if price * balance >= 5000 :
        sell_result = upbit.sell_market_order(coin, balance)
        print(sell_result)
        post_message("매도 체결.\n체결 단가 : "+str(sell_result['price']))

def get_crr(df, fees, K) :
    df['range'] = df['high'].shift(1) - df['low'].shift(1)
    df['targetPrice'] = df['open'] + df['range'] * K
    df['drr'] = np.where(df['high'] > df['targetPrice'], (df['close'] / (1 + fees)) / (df['targetPrice'] * (1 + fees)) , 1)
    return df['drr'].cumprod()[-2]

def get_best_K(coin, fees) :
    df = pyupbit.get_ohlcv(coin, interval = "day", count = 21)
    max_crr = 0
    best_K = 0.5
    for k in np.arange(0.0, 1.0, 0.1) :
        crr = get_crr(df, fees, k)
        if crr > max_crr :
            max_crr = crr
            best_K = k
    return best_K

if __name__ == '__main__': 
    try:
        upbit = pyupbit.Upbit(auth.access, auth.secret)

        # set variables
        coin = "KRW-BTC"
        fees = 0.0005
        K = 0.5
    
        start_balance = upbit.get_balance("KRW")
        df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")
        targetPrice = get_targetPrice(df, get_best_K(coin, fees))
        print(datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S'), "\t\tBalance :", start_balance, "KRW \t\tYield :", ((start_balance / start_balance) - 1) * 100, "% \t\tNew targetPrice :", targetPrice, "KRW")
        post_message("자동매매를 시작합니다.\n잔액 : "+str(start_balance)+" 원\n목표매수가 : "+str(targetPrice))

        while True :
            now = datetime.datetime.now()
            if now.hour == 9 and now.minute == 2 and now.second == 0:    # when am 09:02:00
                sell_all(coin)
                time.sleep(10)

                df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")
                targetPrice = get_targetPrice(df, get_best_K(coin, fees))

                cur_balance = upbit.get_balance("KRW")
                print(now.strftime('%y/%m/%d %H:%M:%S'), "\t\tBalance :", cur_balance, "KRW \t\tYield :", ((cur_balance / start_balance) - 1) * 100, "% \t\tNew targetPrice :", targetPrice, "KRW")
                post_message("새로운 장 시작\n수익률 : "+str(((cur_balance / start_balance) - 1) * 100)+"%\n잔액 : "+str(cur_balance)+"원\n목표매수가 : "+str(targetPrice))
            
            elif targetPrice <= pyupbit.get_current_price(coin) :
                buy_all(coin)
                
                start_time = df.index[-1]
                end_time = start_time + datetime.timedelta(days=1)
                if end_time > now :
                    print((end_time - now).seconds)
                    time.sleep((end_time - now).seconds - 60)
    
            time.sleep(1)

    except Exception as e:
        print(e)
        post_message(e)
        time.sleep(1)
