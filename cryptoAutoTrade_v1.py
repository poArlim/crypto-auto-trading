import pyupbit
import datetime
import time, calendar
import auth             # save 'access key' and 'secret key'

def get_targetPrice(df, K) :
    range = df['high'][-2] - df['low'][-2]
    return df['open'][-1] + range * K

def buy_all(coin) :
    balance = upbit.get_balance("KRW") * 0.9995
    if balance >= 5000 :
        print(upbit.buy_market_order(coin, balance))

def sell_all(coin) :
    balance = upbit.get_balance(coin)
    price = pyupbit.get_current_price(coin)
    if price * balance >= 5000 :
        print(upbit.sell_market_order(coin, balance))


if __name__ == '__main__': 
    try:
        upbit = pyupbit.Upbit(auth.access, auth.secret)

        # set variables
        coin = "KRW-BTC"
        fees = 0.0005
        K = 0.5
    
        start_balance = upbit.get_balance("KRW")
        df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")
        targetPrice = get_targetPrice(df, K)
        print(datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S'), "\t\tBalance :", start_balance, "KRW \t\tYield :", ((start_balance / start_balance) - 1) * 100, "% \t\tNew targetPrice :", targetPrice, "KRW")

        while True :
            now = datetime.datetime.now()
            if now.hour == 9 and now.minute == 0 and now.second == 0:    # when am 09:02:00
                sell_all(coin)
                df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")
                targetPrice = get_targetPrice(df, K)
                time.sleep(1)

                cur_balance = upbit.get_balance("KRW")
                print(now.strftime('%y/%m/%d %H:%M:%S'), "\t\tBalance :", cur_balance, "KRW \t\tYield :", ((cur_balance / start_balance) - 1) * 100, "% \t\tNew targetPrice :", targetPrice, "KRW")
            
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
        time.sleep(1)
