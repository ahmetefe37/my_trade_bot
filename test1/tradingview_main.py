from tradingview_ta import TA_Handler,Interval
from tradingview_symbol_data import *

# print(get_all_symbols())
# coin = TA_Handler(
#     screener="crypto",
#     exchange="BINANCE",
#     symbol="BTCUSDT",
#     interval=Interval.INTERVAL_1_HOUR
# )
# coin.get_indicators()
# indicators = ["Recommend.Other","Recommend.All","Recommend.MA",
#     "RSI","RSI[1]","Stoch.K","Stoch.D","Stoch.K[1]","Stoch.D[1]",
#     "CCI20","CCI20[1]","ADX","ADX+DI","ADX-DI","ADX+DI[1]","ADX-DI[1]",
#     "AO","AO[1]","Mom","Mom[1]","MACD.macd","MACD.signal","Rec.Stoch.RSI",
#     "Stoch.RSI.K","Rec.WR","W.R","Rec.BBPower","BBPower","Rec.UO","UO",
#     "close","EMA5","SMA5","EMA10","SMA10","EMA20","SMA20","EMA30","SMA30",
#     "EMA50","SMA50","EMA100","SMA100","EMA200","SMA200","Rec.Ichimoku",
#     "Ichimoku.BLine","Rec.VWMA","VWMA","Rec.HullMA9","HullMA9",
#     "Pivot.M.Classic.S3","Pivot.M.Classic.S2","Pivot.M.Classic.S1",
#     "Pivot.M.Classic.Middle","Pivot.M.Classic.R1","Pivot.M.Classic.R2",
#     "Pivot.M.Classic.R3","Pivot.M.Fibonacci.S3","Pivot.M.Fibonacci.S2",
#     "Pivot.M.Fibonacci.S1","Pivot.M.Fibonacci.Middle","Pivot.M.Fibonacci.R1",
#     "Pivot.M.Fibonacci.R2","Pivot.M.Fibonacci.R3","Pivot.M.Camarilla.S3",
#     "Pivot.M.Camarilla.S2","Pivot.M.Camarilla.S1","Pivot.M.Camarilla.Middle",
#     "Pivot.M.Camarilla.R1","Pivot.M.Camarilla.R2","Pivot.M.Camarilla.R3",
#     "Pivot.M.Woodie.S3","Pivot.M.Woodie.S2","Pivot.M.Woodie.S1"
#     ,"Pivot.M.Woodie.Middle","Pivot.M.Woodie.R1","Pivot.M.Woodie.R2",
#     "Pivot.M.Woodie.R3","Pivot.M.Demark.S1","Pivot.M.Demark.Middle",
#     "Pivot.M.Demark.R1", "open", "P.SAR", "BB.lower", "BB.upper", "AO[2]", 
#     "volume", "change", "low", "high"]
# data1 = coin.get_analysis().indicators
# data2 = coin.get_analysis().moving_averages
# data3 = coin.get_analysis().oscillators
# data4 = coin.get_analysis().summary
# print(data1)
# print(data2)
# print(data3)
# print(data4)
# data_indicator_rsi = data1["RSI"]
# data_indicator_rsi_old = data1["RSI[1]"]