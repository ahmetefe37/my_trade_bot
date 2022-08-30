from pydoc import cli
from binance import Client
import csv
import pandas as pd
from datetime import datetime as dt

client = Client(None,None)

PERIOD = {
    "1m":client.KLINE_INTERVAL_1MINUTE,
    "3m":client.KLINE_INTERVAL_30MINUTE,
    "5m":client.KLINE_INTERVAL_5MINUTE,
    "15m":client.KLINE_INTERVAL_15MINUTE,
    "30m":client.KLINE_INTERVAL_30MINUTE,
    "1h":client.KLINE_INTERVAL_1HOUR,
    "2h":client.KLINE_INTERVAL_2HOUR,
    "4h":client.KLINE_INTERVAL_4HOUR,
    "6h":client.KLINE_INTERVAL_6HOUR,
    "8h":client.KLINE_INTERVAL_8HOUR,
    "12h":client.KLINE_INTERVAL_12HOUR,
    "1d":client.KLINE_INTERVAL_1DAY,
    "3d":client.KLINE_INTERVAL_3DAY,
    "1w":client.KLINE_INTERVAL_1WEEK,
    "1M":client.KLINE_INTERVAL_1MONTH,
}

def calculateTime(timestamp):
    return dt.fromtimestamp(timestamp / 1000)

def bringData(SYMBOL, PERIOD,START, END):
    data = client.get_historical_klines(SYMBOL,PERIOD,START,END)
    return data

def write2Csv(SYMBOL,PERIOD,DATA):
    filename = str(SYMBOL + "-" + PERIOD + ".csv")
    csvFile = open(filename,"w",newline="")
    writer = csv.writer(csvFile,delimiter=",")
    for singleData in DATA:
        writer.writerow(singleData)
    csvFile.close()
    return filename

def write2Excel(CSV_FILE):
    TITLES = ["open_time","open","high","low","close","vol","close_time","wav","nat","tbbav","ignore","a","b","c","d","e","f","g","h","i"]
    DATA = pd.read_csv(CSV_FILE,names=TITLES)
    DATES = pd.Series(map(lambda x: calculateTime(x).date() , DATA["open_time"]))
    TIMES = pd.Series(map(lambda x: calculateTime(x).time() , DATA["open_time"]))
    TOTAL = pd.DataFrame({
        "DATES":DATES, "TIMES":TIMES, "OPEN_PRICE":DATA["open"], "HIGHEST_PRICE":DATA["high"],
        "LOWEST_PRICE":DATA["low"], "CLOSE_PRICE":DATA["close"], "VOLUME": DATA["vol"], "WAVG":0
    })
    with pd.ExcelWriter(CSV_FILE + ".xlsx") as writer:
        TOTAL.to_excel(writer, sheet_name="file1", index=False)

def setPeriod():
    print("-- PERIODS --")
    for i in PERIOD:
        print(i)
    print("-------------")
    choice = input("Enter a period: ")
    return choice

def setSymbol():
    print("-- Enter a list of coins like this format -> BTCUSDT --")
    coins = []
    while True:
        choice = input("Enter a coin: ")        
        if choice == "":
            break
        else:
            coins.append(choice)
    return coins

def setDate(d):
    print("Enter start and end date like this format -> 01 January 2022")
    if d == 0:
        choice = input("Enter start date: ")
    elif d == 1:
        choice = input("Enter end date: ")
    return choice

def bringData_and_write2Excel(SYMBOL, PERIOD, START, END):
    for COIN in SYMBOL:
        write2Excel(write2Csv(COIN, PERIOD, bringData(COIN,PERIOD,START,END)))
        print(COIN, " - DATA IS PULLED SUCCESSFULLY!")

bringData_and_write2Excel(setSymbol(),setPeriod(),setDate(0),setDate(1))