from binance import Client
import csv
import pandas as pd
from datetime import datetime as dt
import pandas_ta as ta

# reading datas from csv files ----------------------------
client = Client(None,None)

# time converter function ---------------------------------
def calculateTime(timestamp):
    return dt.fromtimestamp(timestamp/1000)

def DCA(url):
    wallet = 100
    buy_count = 0
    sell_count = 0
    coin_amount = 0
    fee_rate = 1/1000
    given_fee = 0

    DATA_FILE = url
    TITLES = ["open_time","open","high","low","close","vol","close_time","wav","nat","tbbav","ignore","a","b","c","d","e","f","g","h","i"]
    DF = pd.read_csv(DATA_FILE,names=TITLES)
    OPEN_PRICE = DF["open"]
    CLOSE_PRICE = DF["close"]
    OPEN_TIME = DF["open_time"]
    CLOSE_TIME = DF["close_time"]
    HIGH_PRICE = DF["high"]
    LOW_PRICE = DF["low"]

    sma50 = ta.sma(CLOSE_PRICE,50)
    print("############################################")
    for i in range(len(CLOSE_PRICE)):
        if pd.isna(sma50[i]) is False:
            if CLOSE_PRICE[i-1] < sma50[i-1] and CLOSE_PRICE[i] > sma50[i]:
                print(wallet / CLOSE_PRICE[i] ," BTC have been bought at ", calculateTime(OPEN_TIME[i]))
                print("----------------------")
                buy_count += 1
                coin_amount = wallet / CLOSE_PRICE[i]
                given_fee += fee_rate * wallet
            if CLOSE_PRICE[i-1] > sma50[i-1] and CLOSE_PRICE[i] < sma50[i] and buy_count > 0:
                print(coin_amount ," BTC have been sold at ", calculateTime(OPEN_TIME[i+1]))
                print("----------------------")
                sell_count += 1
                coin_selled_value = coin_amount * CLOSE_PRICE[i]
                wallet  = coin_selled_value
                coin_amount = 0
                given_fee += fee_rate * coin_selled_value

    print("-----------------------------------")
    print("Total Buy: {} - Sell: {} ".format(buy_count,sell_count))
    print("BTC Count in wallet: ",coin_amount)
    print("Total investment: ", wallet * buy_count)
    print("Total Given Fee: ", given_fee)
    print("Current wallet Value: ", wallet)
    print("-----------------------------------")

DCA("data/BTCUSDT-1h.csv")