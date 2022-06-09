import asyncio
import pandas as pd
import numpy as np
from datetime import datetime


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

async def get_bid_ask(exchange, symbol):
    orderbook = await exchange.fetchOrderBook(symbol)
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    return {'bid': bid, 'ask': ask}

async def get_open_positions(exchange):
    return await exchange.fetchPositions()


def execute_papertrade(coin):
    trade_data = {}

    # close open positions that contradict the market sentiment
    if coin.position['isOpen'] and (coin.position['side'] != coin.market_sentiment):
        date = datetime.now()
        coin.position['side'] = None
        exit_price = coin.get_marketorder_price()
        coin.position['isOpen'] = False
        trade_data = {
            'trade_id': coin.position['trade_id'],
            'date_close': date, 
            'exit': exit_price
            }

    # no open position, enter position according to market sentiment
    if coin.position['isOpen'] == False:
        date = datetime.now()
        coin.position['side'] = coin.market_sentiment
        entry_price = coin.get_marketorder_price()
        coin.increase_id()
        coin.position['isOpen'] = True
        trade_data = {
            'trade_id': coin.trade_id, 
            'date_open': date, 
            'date_close': None,
            'symbol': coin.symbol, 
            'side': coin.position['side'], 
            'entry': entry_price,
            'exit': None
            }


    return trade_data