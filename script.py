import os
import time
from  dotenv import load_dotenv
import asyncio
import tulipy as ti
import ccxt.async_support as ccxt
from coin import Coin
import data
import trading_strategies as ts

# load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
API_PASSWORD = os.getenv('API_PW')

# coins to monitor
watchlist = {
    'ada': Coin('ADA/USDT:USDT'),
    'ape': Coin('APE/USDT:USDT'),
    'avax': Coin('AVAX/USDT:USDT'),
    'btc': Coin('BTC/USDT:USDT'),
    'eth': Coin('ETH/USDT:USDT'),
    'ftm': Coin('FTM/USDT:USDT'),
    'sol': Coin('SOL/USDT:USDT'),
    'xrp': Coin('XRP/USDT:USDT')
}

BULLISH = 1
BEARISH = -1

# connect to kucoin futures broker
exchange = ccxt.kucoinfutures({
    'apiKey': API_KEY,
    'apiSecret': API_SECRET,
    'password': API_PASSWORD
})


async def main():
    # load market data
    await exchange.load_markets()

    while True:
            
        # get price data
        await data.get_candle_data(exchange, watchlist, '5m')

        # get ohlc candles and calculate 12 EMA, and 26 EMA
        for coin in watchlist.values():
            # get ohlc candles
            coin.candles = data.get_ohlc_candle_data(coin.raw_data)

            # calculate 12 EMA and 26 EMA
            coin.ema_12 = ti.ema(coin.candles['close'], period=12)
            coin.ema_26 = ti.ema(coin.candles['close'], period=26)

            # determine whether to LONG, SHORT, or HOLD
            two_ema_advice = ts.two_ema_strategy(coin.ema_12[-1], coin.ema_26[-1])
            
            if (two_ema_advice == BULLISH):
                print(f'Entered long on {coin.symbol}')
            elif (two_ema_advice == BEARISH):
                print(f'Entered short on {coin.symbol}')

        # run every 5 minutes
        print('=================')
        time.sleep(5)

    await exchange.close()

asyncio.run(main())