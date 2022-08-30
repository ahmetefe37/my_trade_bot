########## LEVEL 2 - LEVEL 3 ########## SMA 50 - SMA 200 SUPPORTED RANDOM POSITIONS
import random
from binance import Client
import csv
import pandas as pd
import numpy as np
from datetime import datetime as dt
import pandas_ta as ta

# reading datas from csv files ----------------------------
#client = Client(None,None)

# time converter function ---------------------------------
def calculateTime(timestamp):
    return dt.fromtimestamp(timestamp/1000)

def randomPosition(url):
    DATA_FILE = url
    TITLES = ["open_time","open","high","low","close","vol","close_time","wav","nat","tbbav","ignore","a","b","c","d","e","f","g","h","i"]
    DF = pd.read_csv(DATA_FILE,names=TITLES)
    OPEN_PRICE = DF["open"]
    CLOSE_PRICE = DF["close"]
    OPEN_TIME = DF["open_time"]
    CLOSE_TIME = DF["close_time"]
    HIGH_PRICE = DF["high"]
    LOW_PRICE = DF["low"]

    WALLET_ARR = []

    for j in range(50):
        
        
    
        WALLET = 100
        COIN_AMOUNT = 0
        FEE_RATE = 1/10000
        FEE_AMOUNT = 0

        BUY_VALUE = 0
        BUY_COUNT = 0
        SELL_COUNT = 0

        POS_TYPE = ""
        IN_POS = False

        TP_LIMIT = 0.2
        SP_LIMIT = -1.4

        LEVER = 50

        TP_COUNT = 0
        SP_COUNT = 0

        sma50 = ta.sma(CLOSE_PRICE,50)
        sma200 = ta.sma(CLOSE_PRICE,200)
        price_above_sma50 = None
        price_above_sma200 = None
        sma50_above_sma200 = None

        for i in range(len(CLOSE_PRICE)):     
            randomValue = random.randint(0,3)      
            
            if pd.isna(sma50[i]) is False and pd.isna(sma200[i]) is False and not IN_POS: # sma50 control
                price_above_sma50 = np.where(CLOSE_PRICE[i] > sma50[i], True, False)
                price_above_sma200 = np.where(CLOSE_PRICE[i] > sma200[i], True, False)
                sma50_above_sma200 = np.where(sma50[i] > sma200[i], True, False)

                print("\n##################################")
                if price_above_sma50 == True:
                    randomValue += 1
                    print("SMA50 CONFIRMED")
                else:
                    randomValue -= 1
                    print("SMA50 REFUSED")
                if price_above_sma200 == True:
                    randomValue += 1
                    print("SMA200 CONFIRMED")
                else:
                    randomValue -= 1
                    print("SMA200 REFUSED")
                if sma50_above_sma200 == True:
                    print("SMA50 - SMA200 CROSS CONFIRMED")
                    randomValue += 1
                else:
                    randomValue -= 1
                    print("SMA50 - SMA200 CROSS REFUSED")
                
                print("##################################\n")

            if randomValue > 3: randomValue = 3
            if randomValue < 0: randomValue = 0
            print("RANDOM VALUE: ",randomValue)

            if pd.isna(CLOSE_PRICE[i]) is False:
                if randomValue == 3 and not IN_POS: # long order
                    print(WALLET /CLOSE_PRICE[i] ," BTC have been bought at ", calculateTime(OPEN_TIME[i]))
                    print("----------------------")
                    COIN_AMOUNT = WALLET / CLOSE_PRICE[i]
                    FEE_AMOUNT += FEE_RATE * (WALLET)
                    BUY_COUNT += 1
                    BUY_VALUE = CLOSE_PRICE[i]
                    IN_POS = True
                
                # elif randomValue == 0: # short order
                #     print("enter short..")
                
                
                if IN_POS:
                    buy_val = BUY_VALUE
                    PERCENT_PROFIT = (CLOSE_PRICE[i] - buy_val) / buy_val * 100
                    
                    if PERCENT_PROFIT >= TP_LIMIT:
                        print(WALLET / CLOSE_PRICE[i] ," BTC have been sold at ", calculateTime(OPEN_TIME[i]))
                        
                        NEW_WALLET = COIN_AMOUNT * CLOSE_PRICE[i]
                        WALLET = NEW_WALLET
                        FEE_AMOUNT += FEE_RATE * NEW_WALLET
                        COIN_AMOUNT = 0
                        IN_POS = False
                        SELL_COUNT += 1
                        TP_COUNT += 1

                    if PERCENT_PROFIT <= SP_LIMIT:
                        print(WALLET / CLOSE_PRICE[i] ," BTC have been sold at ", calculateTime(OPEN_TIME[i]))
                        
                        NEW_WALLET = COIN_AMOUNT * CLOSE_PRICE[i]
                        WALLET = NEW_WALLET
                        FEE_AMOUNT += FEE_RATE * NEW_WALLET
                        COIN_AMOUNT = 0
                        IN_POS = False
                        SELL_COUNT += 1 
                        SP_COUNT += 1

        print("\n--------- LAST WALLET ------------") 
        print("Total TP: {} - STOP: {} ".format(TP_COUNT,SP_COUNT))
        print("Total POSITION: {} ".format(BUY_COUNT))
        print("BTC Count in wallet: ",COIN_AMOUNT)
        print("Total investment: ", WALLET * BUY_COUNT)
        print("Total Given Fee: ", FEE_AMOUNT)
        print("Current wallet Value: ", WALLET)
        print("-----------------------------------")

        WALLET_ARR.append(WALLET)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    sum_wallet = 0
    for i in range(len(WALLET_ARR)):
        print("WALLET-",i+1,": ",WALLET_ARR[i])
        sum_wallet += WALLET_ARR[i]
    print("WALLET AVERAGE: ",sum_wallet/len(WALLET_ARR))
        
randomPosition("data/DOTUSDT-1h.csv")