import asyncio
from fileinput import close
import pandas as pd
import numpy as np


async def get_candle_data(exchange, watchlist: dict, timeframe: str, limit=50):
    for coin in watchlist.values():
        await asyncio.sleep(exchange.rateLimit / 1000)      # milliseconds
        coin.raw_data = await exchange.fetchOHLCV(coin.symbol, timeframe, limit=limit)

def get_ohlc_candle_data(raw_data):
    raw_data_arr = np.array(raw_data)                # 2d array with columns: time, open, high, low, close, volume
    
    # select only open, high, low, and close columns
    open_candles = raw_data_arr[:,1]
    high_candles = raw_data_arr[:,2]
    low_candles = raw_data_arr[:,3]
    close_candles = raw_data_arr[:,4]

    # collapse each array into 1d numpy array
    return {
        'open': open_candles.flatten(),
        'high': high_candles.flatten(),
        'low': low_candles.flatten(),
        'close': close_candles.flatten()
    }