import pyupbit
from datetime import datetime
import time, calendar
import math
import auth             # save 'access key' and 'secret key'

upbit = pyupbit.Upbit(auth.access, auth.secret)

def get_targetPrice(df, K) :
    range = df['high'][-2] - df['low'][-2]
    return df['open'][-1] + range * K

def buy_all(df, coin) :
    balance = upbit.get_balance("KRW") - 50
    if balance < 5000 :
        print("not enough money")
        return
    print("buy order")
    print(upbit.buy_market_order(coin, balance))

def sell_all(df, coin) :
    balance = upbit.get_balance(coin)
    price = pyupbit.get_current_price(coin)
    if price * balance > 5000 :
        print("sell order")
        print(upbit.sell_market_order(coin, balance))


if __name__ == '__main__': 
    try:
        # set variables
        coin = "KRW-BTC"
        fees = 0.0005
        targetPrice = 1000000000
        K = 0.5
        
        start_balance = upbit.get_balance("KRW")
        df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")

        print("Start Time : ", datetime.now().strftime('%y/%m/%d %H:%M:%S'))
        print("Coin Name : ", coin)
        print("Start Money : ", start_balance)
        print("-----------------------------------------------------------")

        # 가격 감시를 계속 해야한다.
        while True :
            if datetime.now().hour == 9 and datetime.now().minute == 2 and datetime.now().second == 0:    # when am 09:02:00
                df = pyupbit.get_ohlcv(coin, count = 2, interval = "day")
                order_list = upbit.get_order(coin)
                for i in order_list :
                    upbit.cancel_order(i['uuid'])
                sell_all(df, coin)
                targetPrice = get_targetPrice(df, K)
                cur_balance = upbit.get_balance("KRW")
                print(datetime.now().strftime('%y/%m/%d %H:%M:%S'), "평가금액 :", cur_balance, "KRW, 수익률 :", ((cur_balance / start_balance) - 1) * 100, "%, New targetPrice :", targetPrice)
                time.sleep(1)
            if targetPrice <= pyupbit.get_current_price(coin) :
                buy_all(df, coin)
                
                year = datetime.now().year
                month = datetime.now().month
                day = datetime.now().day

                oddMonth = [1,3,5,7,9,11]
                evenMonth = [4,6,8,10,12]
                if datetime.now().hour < 9 :
                    nextUpdateTime = datetime(year, month, day, 9, 0, 0)
                else :
                    if (month in oddMonth) and (day == 31) :
                        month += 1
                    elif (month in evenMonth) and (day == 30) :
                        if month == 12 :
                            year += 1
                            month = 1
                        else :
                            month += 1
                    elif (month == 2) and (day == 28) :
                        month += 1
                    day = 1
                    nextUpdateTime = datetime(year, month, day, 9, 0, 0)

                time.sleep((nextUpdateTime - datetime.now()).seconds)
            time.sleep(0.1)

    except Exception as ex:
        print("Error!")
        sys.exit(0)
