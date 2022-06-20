import asyncio
import numpy as np
from coin import Coin


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
    if coin.open_position_contradicts_sentiment():
        trade_data['closed_position'] = coin.close_trade()

    # no open position, enter position according to market sentiment
    if coin.position['isOpen'] == False:
        trade_data['opened_position'] = coin.open_trade()

    print(trade_data)
    return trade_data

def get_coin_leverage_limits(exchange, coin) -> list:
    market_data = exchange.markets[coin.symbol]
    return [market_data['limits']['leverage']['min'], market_data['limits']['leverage']['max']]
       
def get_coin_contract_size(exchange, coin):
    market_data = exchange.markets[coin.symbol]
    return market_data['contractSize']

def get_coins_contract_data(exchange, watchlist):
    for coin in watchlist.values():
        coin.contract_size = get_coin_contract_size(exchange, coin)
        coin.leverage_limits['min'], coin.leverage_limits['max'] = get_coin_leverage_limits(exchange, coin)

def verify_perp_market(exchange, symbol):
    market_data = exchange.markets[symbol]
    if market_data['type'] != 'swap':
        return False
    return True

def verify_watchlist(exchange, watchlist: list) -> dict:
    verified_coins = {}

    for symbol in watchlist:
        # check if symbol retrieves perpetual futures market
        retrieves_perp_market = verify_perp_market(exchange, symbol)

        if retrieves_perp_market:
            key = symbol.split('/')[0]
            verified_coins[key] = Coin(symbol)
        else:
            print(f'Market data for {symbol} is not for perp!')

    return verified_coins            

