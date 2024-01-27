#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:05:24 2023

@author: be
"""
from CONFIG import CONFIG

from binance.client import Client
import pandas as pd


def getInfo():
    k, s = CONFIG()
    client = Client(k,s)
    print(client.get_account())

        
def getBalance():
    data = {'coin':['BTC'], 'amount':[0.0], 'actVal':[0.0]}
    portfolio = pd.DataFrame(data)
    portfolio.set_index("coin", inplace = True)
    try:
        portfolio = pd.read_pickle("balance.txt")
    except Exception as error:
        portfolio.to_pickle("balance.txt")
        print(error)
    return portfolio
        
def getPrice(client, sym):
    currentTickers = client.get_all_tickers()
    
    def getFittingPrice(sym):
        for i in currentTickers:
            if sym == i["symbol"]:
                return float(i["price"])
    return getFittingPrice(sym)

def get_filter(symbol):
    k, s = CONFIG()
    client = Client(k,s)
    data_from_api = client.get_exchange_info()
    symbol_info = next(filter(lambda x: x['symbol'] == symbol, data_from_api['symbols']))
    
    return symbol_info
