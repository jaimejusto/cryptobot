import asyncio
import numpy as np
from coin import Coin


async def _get_candle_data(exchange, symbol, timeframe: str, limit=50) -> dict:
    await asyncio.sleep(exchange.rateLimit / 1000)      # milliseconds
    raw_data = await exchange.fetchOHLCV(symbol, timeframe, limit=limit)
    candles = _clean_ohlc_candle_data(raw_data)
    return candles

def _clean_ohlc_candle_data(raw_data) -> dict:
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

async def _get_bid_ask(exchange, symbol) -> dict:
    orderbook = await exchange.fetchOrderBook(symbol)
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    return {'bid': bid, 'ask': ask}

async def get_price_data(exchange, coin, timeframe: str) -> list:
    candles = await _get_candle_data(exchange, coin, timeframe)
    marketprice = await _get_bid_ask(exchange, coin)
    return [candles, marketprice]

async def get_open_positions(exchange):
    return await exchange.fetchPositions()

def execute_papertrade(coin, balance, risk, leverage):
    trade_data = {}

    # close open positions that contradict the market sentiment
    if coin.open_position_contradicts_sentiment():
        trade_data['closed_position'] = coin.close_trade()

    # no open position, enter position according to market sentiment
    if not coin.has_open_position():
        if not _paperfunds_available(balance):
            print(f'No balance available to open new positions.')
            return trade_data
        
        usable_buying_power = _get_usable_buying_power(coin, balance, risk, leverage)
        price_per_contract = coin.get_contract_cost()
        funds_required = _get_collateral(balance, risk)
        if not _able_to_open_min_position(usable_buying_power, price_per_contract):
            print(f'Balance: ${balance}. Not enough to open {coin.symbol} position.')
            return trade_data

        position_size = _get_position_size(usable_buying_power, coin.contract_size, price_per_contract)
        trade_data['opened_position'] = coin.open_trade(funds_required, position_size)

    print(trade_data)
    return trade_data

def _get_coin_leverage_limits(exchange, coin) -> list:
    market_data = exchange.markets[coin]
    return [market_data['limits']['leverage']['min'], market_data['limits']['leverage']['max']]
       
def _get_coin_contract_size(exchange, coin):
    market_data = exchange.markets[coin]
    multiplier = 1 if 'multiplier' not in market_data else market_data['multiplier']
    return market_data['contractSize'] * multiplier

def _get_taker_fee_rate(exchange, coin):
    market_data = exchange.markets[coin]
    return market_data['info']['takerFeeRate']

def get_coins_contract_data(exchange, watchlist: list) -> dict:
    verified_coins = {}

    for symbol in watchlist:
        # check if symbol retrieves perpetual futures market
        if _retrieves_perp_market(exchange, symbol):
            contract_size = _get_coin_contract_size(exchange, symbol)
            min_leverage, max_leverage = _get_coin_leverage_limits(exchange, symbol)
            taker_fee_rate = _get_taker_fee_rate(exchange, symbol)

            key = symbol.split('/')[0]
            verified_coins[key] = Coin(symbol, contract_size, min_leverage, max_leverage, taker_fee_rate)
        else:
            print(f'{symbol} not found in futures market!')
    
    return verified_coins

def _retrieves_perp_market(exchange, symbol):
    market_data = exchange.markets[symbol]
    if market_data['type'] != 'swap':
        return False
    return True  

def _paperfunds_available(balance):
    return balance > 0
    
def _get_usable_buying_power(coin, balance, risk, leverage):
    buying_power = _get_buying_power(balance, risk, leverage)
    taker_fees = _get_taker_fees(buying_power, coin.taker_fee_rate)
    return buying_power - taker_fees

def _get_collateral(balance, risk):
    return balance * risk

def _get_buying_power(balance, risk, leverage):
    collateral = _get_collateral(balance, risk)
    return collateral * leverage

def _get_taker_fees(taker_fee_rate, buying_power):
    return buying_power * taker_fee_rate

def _able_to_open_min_position(usable_buying_power, contract_cost):
    return usable_buying_power > contract_cost

def _get_position_size(usable_buying_power, contract_size, contract_cost):
    num_contracts = usable_buying_power // contract_cost
    return num_contracts * contract_size
