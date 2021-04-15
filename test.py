import pyupbit
from datetime import datetime
import time, calendar
import math
import auth             # save 'access key' and 'secret key'

upbit = pyupbit.Upbit(auth.access, auth.secret)

def get_average(coin, count, interval) :
    df = pyupbit.get_ohlcv(coin, count = count, interval = interval)
    avg = sum(df.close) / count
    return avg

def sell_limit_all(coin) :
    cancle_all(coin)
    balance = upbit.get_balance(coin)
    dest_price = get_average(coin, count, interval)
    print("Sell order : ", upbit.sell_limit_order(coin, balance, dest_price))

def buy_limit_all(coin, fees) :
    cancle_all(coin)
    balance = upbit.get_balance("KRW")
    dest_price = get_average(coin, count, interval)
    amount = (balance - math.ceil(balance * fees)) / dest_price
    print("Buy order : ",upbit.buy_limit_order(coin, dest_price, amount))

def sell_market_all(coin) :
    balance = upbit.get_balance(coin)
    if balance > 0 :
        #print("datetime.now().strftime('%yyyy%m/%d %H:%M:%S')")
        sell = upbit.sell_market_order(coin, balance)
        print(sell['created_at'], "sell", sell['locked'], coin)

def buy_market_all(coin) :
    balance = math.floor(upbit.get_balance("KRW")) - 50
    if balance >= 5000 :
        #print("datetime.now().strftime('%y%m/%d %H:%M:%S')")
        buy = upbit.buy_market_order(coin, balance)
        print(buy['created_at'], "buy", buy['locked'], "won")

def cancle_all(coin) :
    order_list = upbit.get_order(coin)
    for i in order_list :
        print("Cancle order : ",upbit.cancel_order(i['uuid']))


if __name__ == '__main__': 
    try:
        # set variables
        coin = "KRW-BTC"
        count = 5
        interval = "minute15"
        fees = 0.0005
        std_diff = 40000

        print("Start Time : ", datetime.now().strftime('%y/%m/%d %H:%M:%S'))
        print("Coin Name : ", coin)
        print("Start Money : ", upbit.get_balance("KRW"))
        print("-----------------------------------------------------------")

        while True :
            cur_price = pyupbit.get_current_price(coin)
            dest_price = get_average(coin, count, interval)
            diff = cur_price - dest_price
            if diff <= std_diff and diff >= (std_diff * -1) :
                time.sleep(0.5)
                continue
            else :
                if cur_price < dest_price :     # diff < 0
                    sell_market_all(coin)
                    time.sleep(1)
                elif cur_price > dest_price :   # diff > 0
                    buy_market_all(coin)
                    time.sleep(1)
            time.sleep(1)

    except Exception as ex:
        print("Error!")
        sys.exit(0)
