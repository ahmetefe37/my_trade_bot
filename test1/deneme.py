from importlib.resources import open_text
from operator import length_hint
from binance import Client
import csv
import pandas as pd
from datetime import datetime as dt
import pandas_ta as ta

# creating a client ------------------------------------------
client = Client(None,None) # api_key, api_secret

# defination of symbol --------------------------------------
COIN = ["BTCUSDT","ETHUSDT","BNBUSDT","ADAUSDT","SOLUSDT"]

# defination canlesb------------------------------------------
# symbol, time interval, start point, end point, limit, klines type
# candles = client.get_historical_klines(COIN,client.KLINE_INTERVAL_1DAY,"22 August 2020","22 August 2022")
# print(candles)

# function of candles -----------------------------------------
def bringData(symbol,period,start,end):
    candles = client.get_historical_klines(symbol,period,start,end)
    return candles

# writing coin prices on csv files -----------------------------
def writeCsv(symbol,data):
    csvFile = open(symbol + ".csv" , "w",newline="")
    writer = csv.writer(csvFile,delimiter=',')
    for singleData in data:
        writer.writerow(singleData)
    csvFile.close()

# using functions above --------------------------------------
def bringData_writeCsv():
    for coin in COIN:
        writeCsv(coin,bringData(coin,client.KLINE_INTERVAL_1DAY,"01 January 2021","01 January 2022"))

# downloading csv files of coins
#bringData_writeCsv()

# reformatting the time format ----------------------------------
def calculateTime(timestamp):
    return dt.fromtimestamp(timestamp/1000)

# using two func in one command -----------------------------
#writeCsv(COIN,bringData(COIN,client.KLINE_INTERVAL_1DAY,"01 January 2022","01 August 2022"))

# splitting parts of main csv files  -------------------------
willReadCsv = "BTCUSDT.csv"

titles = ["id","open_time","open","high","low","close","vol","close_time","wav","nat","tbqav","ignore"]

# data frame from pandas
df = pd.read_csv(willReadCsv,names=titles)

open_price = df["open"]
close_price = df["close"]

opening_time = df["open_time"]
closing_time = df["close_time"]

high_price = df["high"]
low__price = df["low"]

# function of showing time
def showOpenTime():
    for i in opening_time:
        print(calculateTime(i))

#showOpenTime()

# calculating the RSI values -------------------------
def showRSI():
    period = 14
    rsi_values = ta.rsi(close_price,period)
    print(rsi_values)

#showRSI()

# calculating the moving avarage values
def showMA():
    mov_avg = ta.ma("sma",close_price,length=50)
    print(mov_avg)

#showMA()

# calculating the adx values
def showADX():
    period = 14
    adx = ta.adx(high_price,low__price,close_price,period)
    print(adx)

#showADX()

# calculating the macd values
def showMACD():
    fast, slow, signal = 12, 26, 9
    macd = ta.macd(close_price,fast,slow,signal)
    print(macd)

#showMACD()

def showBollinger():
    length, std = 20, 2
    bollinger = ta.bbands(close_price,length,std)
    print(bollinger)

#showBollinger()