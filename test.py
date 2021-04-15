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

        print("시작 시간 : ", datetime.now().strftime('%m/%d %H:%M:%S'))
        print("종목명 : ", coin)
        print("시작 금액 : ", upbit.get_balance("KRW"))

        while True :
            cur_price = pyupbit.get_current_price(coin)
            dest_price = get_average(coin, count, interval)

            if cur_price < dest_price :
                buy_all(coin, fees)
            elif cur_price > dest_price :
                sell_all(coin)



    except Exception as ex:
        dbgout('`main -> exception! ' + str(ex) + '`')



        while True:
            if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15 : 매수
                for sym in symbol_list:
                    if len(bought_list) < target_buy_count:
                        buy_etf(sym)
                        time.sleep(1)
                if t_now.minute == 30 and 0 <= t_now.second <= 5: 
                    get_stock_balance('ALL')
                    time.sleep(5)
            if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
                if sell_all() == True:
                    dbgout('`sell_all() returned True -> self-destructed!`')
                    sys.exit(0)
            if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
                dbgout('`self-destructed!`')
                sys.exit(0)
            time.sleep(3)
