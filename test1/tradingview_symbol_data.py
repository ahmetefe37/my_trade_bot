from urllib.parse import urljoin, urlencode
import requests as r
import pandas as pd
import pandas_ta as ta
from getmac import get_mac_address as gma
import hmac, hashlib, json, time, urllib.request, requests

# BINANCE INFOS
BASE_URL = "https://fapi.binance.com/fapi/"
SECRET_KEY = "yourbinancesecretkey"
API_KEY = "yourbinanceapikey"

# bring all datas of an symbol
def get_data_symbols(symbol, period, limit):
    params = {"symbol":symbol, "interval":period, "limit":limit, "timestamp":timestamp()}
    query_string = urlencode(params)
    url = urljoin(BASE_URL, "v1/klines/")
    payload = {}
    headers = {"Content-Type":"application/json"}
    response = r.request("GET",url, headers=headers, params=params).json()
    converted = pd.DataFrame(response,
                            columns=["open_time","open","high","low","close","vol","close_time","qav","not","tbbav","tbqav","ignore"],
                            dtype=float)
    return converted

# signature test function
# def denemeFonk(symbol, period, limit):
#     params = {"symbol":symbol, "period":period, "limit":limit, "timestamp":timestamp()}
#     query_string = urlencode(params)
#     params["signature"] = hmac.new(SECRET_KEY.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
#     url = urljoin(BASE_URL, "/futures/data/takerlongshortRatio")
#     payload = {}
#     headers = {"Content-Type":"application/json", "X-MBX-APIKEY":API_KEY}
#     response = r.request("GET",url, headers=headers, params=params).json()
#     return response

class Altcoin:
    def __init__(self,amount,coin,interval,limit,stoploss_percent,secret_key,api_key,leverage,margintype):
        self.amount = amount
        self.coin = coin
        self.interval = interval
        self.limit = limit
        self.stoploss_percent = stoploss_percent
        self.secret_key = secret_key
        self.api_key = api_key
        self.leverage = leverage
        self.margintype = margintype

    # margin type function
    def margin_type(self):
        params = {"symbol":self.coin, "marginType":self.margintype, "timestamp":timestamp()}
        query_string = urlencode(params)
        params["signature"] = hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/marginType")
        payload = {}
        headers = {"Content-Type":"application/json", "X-MBX-APIKEY":self.api_key}
        response = r.request("POST",url, headers=headers, params=params).json()
        return response

    # set a leverage
    def leverage(self):
        params = {"symbol":self.coin, "leverage":self.leverage, "timestamp":timestamp()}
        query_string = urlencode(params)
        params["signature"] = hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/leverage")
        payload = {}
        headers = {"Content-Type":"application/json", "X-MBX-APIKEY":self.api_key}
        response = r.request("POST",url, headers=headers, params=params).json()
        return response

    # checking position informations
    def position_infos(self):
        params = {"symbol":self.coin,"timestamp":timestamp()}
        query_string = urlencode(params)
        params["signature"] = hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/positionRisk")
        payload = {}
        headers = {"Content-Type":"application/json", "X-MBX-APIKEY":self.api_key}
        response = r.request("GET",url, headers=headers, params=params).json()
        converted = pd.DataFrame(response)
        return converted
    
    # sending a trade order
    def send_order(self, position, type):
        params = {"symbol":self.coin, "side":position,
                "type":type, "quantity":self.amount,
                "workingType":"CONTRACT_PRICE",
                "timestamp":timestamp(), "positionSide":"BOTH",
                "callbackRate":self.stoploss_percent}
        query_string = urlencode(params)
        params["signature"] = hmac.new(SECRET_KEY.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/order")
        payload = {}
        headers = {"Content-Type":"application/json", "X-MBX-APIKEY":API_KEY}
        response = r.request("POST",url, headers=headers, params=params).json()
        return response

    # checking are we in a position
    def is_in_position(self):
        info = self.position_infos()["entryPrice"][0]
        if info > 0: return True
        else: return False

    # close position with limit orders
    def limit_close_position(self,position,type):
        if position == "long": self.send_order("SELL",type)
        elif position == "short": self.send_order("BUY",type)
    # close position with market orders
    def market_close_position(self,position):
        if position == "long": self.send_order("SELL","MARKET")
        elif position == "short": self.send_order("BUY","MARKET")
    
    # limit open long position
    def limit_open_long_position(self,type):
        self.send_order("BUY",type)
    # market open long position
    def limit_open_long_position(self):
        self.send_order("BUY","MARKET")
        # limit open long position
    def limit_open_short_position(self,type):
        self.send_order("SELL",type)
    # market open long position
    def limit_open_short_position(self):
        self.send_order("SELL","MARKET")

    # my trade history
    def trade_history(self):
        params = {"symbol":self.coin,"incomeType":"REALIZED_PNL","limit":self.limit,"timestamp":timestamp()}
        query_string = urlencode(params)
        params["signature"] = hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/income")
        payload = {}
        headers = {"Content-Type":"application/json", "X-MBX-APIKEY":self.api_key}
        response = r.request("GET",url, headers=headers, params=params).json()
        converted = pd.DataFrame(response)
        return converted

    # calculating profit in X position
    def profit(self,profit_range):
        profit = 0
        for counter in range(0,profit_range):
            profit += self.trade_history["income"][counter]
        result = str("Total profit last " + profit_range + "positions: " + profit)
        return result

    # trailing stop loss order
    def trailing_stoploss(self,position):
        if position == "long": self.send_order("SELL","TRAILING_STOP_MARKET")
        elif position == "short": self.send_order("BUY","TRAILING_STOP_MARKET")

    # canceling an position existed
    def cancel_order(self):
        params = {"symbol":self.coin, "timestamp":timestamp()}
        query_string = urlencode(params)
        params["signature"] = hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/allOpenOrders")
        payload = {}
        headers = {"Content-Type":"application/json", "X-MBX-APIKEY":self.api_key}
        response = r.request("GET",url, headers=headers, params=params).json()
        converted = pd.DataFrame(response)
        return converted

    def open_orders(self):
        params = {"symbol":self.coin, "timestamp":timestamp()}
        query_string = urlencode(params)
        params["signature"] = hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/openOrders")
        payload = {}
        headers = {"Content-Type":"application/json", "X-MBX-APIKEY":self.api_key}
        response = r.request("GET",url, headers=headers, params=params).json()
        converted = pd.DataFrame(response,dtype=float)
        return converted

# list full of symbols in spot and futures
def get_all_symbols():
    response = urllib.request.urlopen(f"{BASE_URL}v1/exchangeInfo").read()
    return list(map(lambda symbol: symbol["symbol"], json.loads(response)["symbols"]))

# bring datas about futures trading infos of a symbol
def get_buy_sell_volume(symbol,period,limit):
    params = {"symbol":symbol, "period":period, "limit":limit, "timestamp":timestamp()}
    query_string = urlencode(params)
    url = urljoin(BASE_URL, "/futures/data/takerlongshortRatio")
    payload = {}
    headers = {"Content-Type":"application/json"}
    response = r.request("GET",url, headers=headers, params=params).json()
    converted = pd.DataFrame(response)
    return converted

# current timestamp function
def timestamp():
    return int(time.time() * 1000 )


# an idea for licensing
# def get_licensed():
#     mac_adress = gma()
#     print("Your MAC Adress: ",mac_adress)
#     site = "https://*****/license.json"
#     headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111"
#     "Safari/537.36 Edg/86.0.622.58",
#     }
#     response = requests.get(site,headers=headers).json()
#     converted = pd.DataFrame(response)
#     list = []
#     for i in range(len(converted["computers"])):
#         list.append(converted["computers"][i]["mac"])
#     if mac_adress in list: return True
#     else: return False
