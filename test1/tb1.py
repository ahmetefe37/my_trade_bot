######## LEVEL 0 ##########
from binance import Client
import csv
import pandas as pd
from datetime import datetime as dt
import pandas_ta as ta

# reading datas from csv files ----------------------------
client = Client(None,None)
DATA_FILE = "data/BTCUSDT-1h.csv"
TITLES = ["open_time","open","high","low","close","vol","close_time","wav","nat","tbbav","ignore","a","b","c","d","e","f","g","h","i"]
DF = pd.read_csv(DATA_FILE,names=TITLES)
OPEN_PRICE = DF["open"]
CLOSE_PRICE = DF["close"]
OPEN_TIME = DF["open_time"]
CLOSE_TIME = DF["close_time"]
HIGH_PRICE = DF["high"]
LOW_PRICE = DF["low"]

# time converter function ---------------------------------
def calculateTime(timestamp):
    return dt.fromtimestamp(timestamp/1000)

# indikator functions -------------------------------------

# RSI ----------------
def showRSI(OPT_MIN_VALUE,OPT_MAX_VALUE,BOUND_PERCENTAGE,CLOSE_PRICE,PERIOD):
    OPT_MIN_VALUE = OPT_MIN_VALUE
    OPT_MAX_VALUE = OPT_MAX_VALUE
    BOUND_PERCENTAGE = BOUND_PERCENTAGE
    IN_UPPER_SIDE = False
    IN_LOWER_SIDE = False
    POS_TYPE = ""
    CONFIRMED = False
    RSI_VALUE = ta.rsi(CLOSE_PRICE,PERIOD)

    # Calculating the optimum upper and lower price gaps
    UPPER_BOUND_GAP = [OPT_MAX_VALUE + (OPT_MAX_VALUE * BOUND_PERCENTAGE),
                                        OPT_MAX_VALUE - (OPT_MAX_VALUE * BOUND_PERCENTAGE)]
    LOWER_BOUND_GAP = [OPT_MIN_VALUE + (OPT_MIN_VALUE * BOUND_PERCENTAGE),
                                        OPT_MIN_VALUE - (OPT_MIN_VALUE * BOUND_PERCENTAGE)]

    # checking if rsi is in the upper and lower price gaps
    if RSI_VALUE < UPPER_BOUND_GAP[0] and RSI_VALUE > UPPER_BOUND_GAP[1]:
        IN_UPPER_SIDE = True
    else:
        IN_UPPER_SIDE = False
    if RSI_VALUE < LOWER_BOUND_GAP[0] and RSI_VALUE > LOWER_BOUND_GAP[1]:
        IN_LOWER_SIDE = True
    else:
        IN_LOWER_SIDE = False

    # specify the position type accordiing to values above
    if IN_UPPER_SIDE:
        POS_TYPE = "SHORT"
        CONFIRMED = True
    else:
        POS_TYPE = ""
        CONFIRMED = False
    if IN_LOWER_SIDE:
        POS_TYPE = "LONG"
        CONFIRMED = True
    else:
        POS_TYPE = ""
        CONFIRMED = False

    print(RSI_VALUE)

    # returning an array that includes rsi value and pos type
    return [RSI_VALUE,POS_TYPE,CONFIRMED]

# SMA ----------------
def showSMA(CLOSE_PRICE,LENGTH):
    SMA_VALUE = ta.sma(CLOSE_PRICE,LENGTH)
    # returning an array that includes sma value and cross type
    return SMA_VALUE

# EMA ----------------
def showEMA(CLOSE_PRICE,LENGTH):
    EMA_VALUE = ta.ema(CLOSE_PRICE,length=LENGTH)
    # returning an array that includes sma value and cross type
    return EMA_VALUE

# ADX ----------------
def showADX(HIGH_PRICE,LOW_PRICE,CLOSE_PRICE,PERIOD):
    ADX_VALUE = ta.adx(HIGH_PRICE,LOW_PRICE,CLOSE_PRICE,PERIOD)
    print(ADX_VALUE)
    return ADX_VALUE

# MACD ---------------
def showMACD(CLOSE_PRICE,FAST,SLOW,SIGNAL):
    MACD_VALUE = ta.macd(CLOSE_PRICE,FAST,SLOW,SIGNAL)
    print(MACD_VALUE)
    return MACD_VALUE

# Bollinger ----------
def showBollinger(CLOSE_PRICE,LENGTH,STD):
    BOLLINGER_VALUE = ta.bbands(CLOSE_PRICE,LENGTH,STD)
    print(BOLLINGER_VALUE)
    return BOLLINGER_VALUE

# KDJ ----------------
def showKDJ(HIGH,LOW,CLOSE_PRICE):
    KDJ_VALUE = ta.kdj(high=HIGH, low=LOW, close=CLOSE_PRICE)

    print("KDJ: ",KDJ_VALUE)
    # return KDJ_VALUE

# strategic trading functions -----------------------------

confirmations = []

def ind_confirm():
    confirms = 0
    for i in ind_confirm:
        if i == True:
            confirms += 1
    if confirms > 3:
        return True
    else:
        False

# Program Loop is starting here --------------------------

def ProgramLoop(CLOSE_PRICE):
    PURCHASE_SIZE = 100
    WALLET_VALUE = 0
    COIN_AMOUNT = 0
    FEE_RATE = 1/1000
    FEE_AMOUNT = 0

    POS_COUNT = 0
    GOLDEN = 0
    DEATH = 0

    IN_POS = False
    CROSS_TYPE = ""
    POS_INPUT_PRICE = CLOSE_PRICE[0]

    SMA50_VALUE = showSMA(CLOSE_PRICE,50)
    SMA200_VALUE = showSMA(CLOSE_PRICE,200)
    #sma - price cross detector
    for c in range(len(CLOSE_PRICE)):
        if pd.isna(SMA50_VALUE[c]) is False and pd.isna(SMA200_VALUE[c]) is False:
            # ma50 golder cross
            # if CLOSE_PRICE[c-1] < SMA50_VALUE[c-1] and CLOSE_PRICE[c] > SMA50_VALUE[c]:
            #     CROSS_TYPE = "GOLDEN"
            # else:
            #     CROSS_TYPE = ""
            # # ma50 death cross
            # if CLOSE_PRICE[c-1] > SMA50_VALUE[c-1] and CLOSE_PRICE[c] < SMA50_VALUE[c]:
            #     CROSS_TYPE = "DEATH"
            # else:
            #     CROSS_TYPE = ""
            # ma200 golder cross
            # if CLOSE_PRICE[c-1] < SMA200_VALUE[c-1] and CLOSE_PRICE[c] > SMA200_VALUE[c]:
            #     CROSS_TYPE = "GOLDEN"
            # else:
            #     CROSS_TYPE = ""
            
            # # ma200 death cross
            # if CLOSE_PRICE[c-1] > SMA200_VALUE[c-1] and CLOSE_PRICE[c] < SMA200_VALUE[c]:
            #     CROSS_TYPE = "DEATH"
            # else:
            #     CROSS_TYPE = ""

            # ma50 - ma200 cross
            if SMA50_VALUE[c-1] < SMA200_VALUE[c-1] and SMA50_VALUE[c] > SMA200_VALUE[c]: # sma50 - sma200 mega golden cross
                CROSS_TYPE = "GOLDEN"
                GOLDEN += 1
            if SMA50_VALUE[c-1] > SMA200_VALUE[c-1] and SMA50_VALUE[c] < SMA200_VALUE[c]: # sma50 - sma200 mega death cross
                CROSS_TYPE = "DEATH"
                DEATH += 1
            
            if CROSS_TYPE == "GOLDEN" and not IN_POS:
                COIN_AMOUNT += (WALLET_VALUE + PURCHASE_SIZE) / CLOSE_PRICE[c]
                FEE_AMOUNT += CLOSE_PRICE * FEE_RATE * COIN_AMOUNT
                WALLET_VALUE = COIN_AMOUNT * CLOSE_PRICE[c] - FEE_AMOUNT
                

                MOV_PERCENTAGE = (( POS_INPUT_PRICE - CLOSE_PRICE[c])/POS_INPUT_PRICE) * 100
                POS_COUNT += 1
                IN_POS = True
                CROSS_TYPE = ""
                print("FIYAT FARKI: ",( POS_INPUT_PRICE - CLOSE_PRICE[c]))
                print("yüzde: ", MOV_PERCENTAGE)

                if MOV_PERCENTAGE >= 0.3:
                    FEE_AMOUNT += FEE_RATE * COIN_AMOUNT * CLOSE_PRICE[c]
                    WALLET_VALUE = COIN_AMOUNT * CLOSE_PRICE[c] - FEE_AMOUNT
                    COIN_AMOUNT = 0
                    IN_POS = False
                elif MOV_PERCENTAGE <= -0.1:
                    FEE_AMOUNT = FEE_RATE * COIN_AMOUNT * CLOSE_PRICE[c]
                    WALLET_VALUE = COIN_AMOUNT * CLOSE_PRICE[c] - FEE_AMOUNT
                    COIN_AMOUNT = 0
                    IN_POS = False
                POS_INPUT_PRICE = CLOSE_PRICE[c]
            # if CROSS_TYPE == "DEATH" and IN_POS:
            #     FEE_AMOUNT = FEE_RATE * COIN_AMOUNT * CLOSE_PRICE[c]
            #     WALLET_VALUE = COIN_AMOUNT * CLOSE_PRICE[c] - FEE_AMOUNT
            #     COIN_AMOUNT = 0
            #     IN_POS = False


    print("--------- LAST WALLET ------------") 
    print("WALLET VALUE: ",WALLET_VALUE[len(CLOSE_PRICE)-1])
    print("TOTAL POSITIONS: ",POS_COUNT)
    print("FEE AMOUNT: ",FEE_AMOUNT[len(CLOSE_PRICE)-1])
    print("----------------------------------")
ProgramLoop(CLOSE_PRICE)