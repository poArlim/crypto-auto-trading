import pyupbit
from datetime import datetime
import time
import auth             # save 'access key' and 'secret key'

def get_targetPrice(df, K) :
    range = df['high'][-2] - df['low'][-2]
    return df['open'][-1] + range * K

def buy_all(coin) :
    balance = upbit.get_balance("KRW") * 0.9995
    if balance < 5000 :
        print("not enough money")
        return
    print("buy order")
    print(upbit.buy_market_order(coin, balance))
    #upbit.buy_market_order(coin, balance)

def sell_all(coin) :
    balance = upbit.get_balance(coin) * 0.9995
    price = pyupbit.get_current_price(coin)
    if price * balance > 5000 :
        print("sell order")
        print(upbit.sell_market_order(coin, balance))
        #upbit.sell_market_order(coin, balance)


if __name__ == '__main__': 
    try:
        upbit = pyupbit.Upbit(auth.access, auth.secret)

        # set variables
        coin = "KRW-BTC"
        fees = 0.0005
        K = 0.5
    
        start_balance = upbit.get_balance("KRW")

        sell_all(coin)
        df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")
        targetPrice = get_targetPrice(df, K)
        print(datetime.now().strftime('%y/%m/%d %H:%M:%S'), "\t\tBalance :", start_balance, "KRW \t\tYield :", ((start_balance / start_balance) - 1) * 100, "% \t\tNew targetPrice :", targetPrice, "KRW")

        while True :
            if datetime.now().hour == 9 and datetime.now().minute == 2 and datetime.now().second == 0:    # when am 09:02:00
                sell_all(coin)
                df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")
                targetPrice = get_targetPrice(df, K)
                
                cur_balance = upbit.get_balance("KRW")
                print(datetime.now().strftime('%y/%m/%d %H:%M:%S'), "\t\tBalance :", cur_balance, "KRW \t\tYield :", ((cur_balance / start_balance) - 1) * 100, "% \t\tNew targetPrice :", targetPrice, "KRW")
                time.sleep(1)
            
            if targetPrice <= pyupbit.get_current_price(coin) :
                buy_all(df, coin)
                
                start_time = df.index[-1]
                now = datetime.datetime.now()
                end_time = start_time + datetime.timedelta(days=1)
                if end_time > now :
                    time.sleep((end_time - now).seconds)
            
            time.sleep(0.1)

    except Exception as e:
        print(e)
        time.sleep(1)
