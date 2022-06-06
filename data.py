import asyncio
import pandas as pd
import numpy as np


async def get_candle_data(exchange, watchlist: dict, timeframe: str, limit=50):
    for coin in watchlist.values():
        await asyncio.sleep(exchange.rateLimit / 1000)      # milliseconds
        coin.raw_data = await exchange.fetchOHLCV(coin.symbol, timeframe, limit=limit)

def get_ohlc_candle_data(raw_data):
    raw_data_arr = np.array(raw_data)                # 2d array with columns: time, open, high, low, close, volume
    ohlc_candles = raw_data_arr[:,1: -1]             # remove time and volume data
    ohlc_df = pd.DataFrame(ohlc_candles, columns=['open', 'high', 'low', 'close'])
    return {
        'open': ohlc_df['open'].tolist(),
        'high': ohlc_df['high'].tolist(),
        'low': ohlc_df['low'].tolist(),
        'close': ohlc_df['close'].tolist()
    }