import pyupbit
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
    cancle_all(coin)
    balance = upbit.get_balance(coin)
    print("Sell market order : ", upbit.sell_market_order(coin, balance))

def buy_market_all(coin) :
    cancle_all(coin)
    balance = upbit.get_balance("KRW")
    print("Buy market order : ", upbit.buy_market_order(coin, balance))

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
        std_diff = 25000

        print("시작 시간 : ", datetime.now().strftime('%m/%d %H:%M:%S'))
        print("종목명 : ", coin)
        print("시작 금액 : ", upbit.get_balance("KRW"))

        while True :
            cur_price = pyupbit.get_current_price(coin)
            dest_price = get_average(coin, count, interval)
            diff = cur_price - dest_price
            if diff <= std_diff and diff >= (std_diff * -1) :
                continue
            else :
                if cur_price < dest_price :     # diff < 0
                    sell_market_all(coin)
                    time.sleep(1)
                elif cur_price > dest_price :   # diff > 0
                    buy_market_all(coin)
                    time.sleep(1)

    except Exception as ex:
        dbgout('`main -> exception! ' + str(ex) + '`')
