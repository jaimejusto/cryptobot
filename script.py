import os
import ccxt.async_support as ccxt
from  dotenv import load_dotenv
import asyncio
from coin import Coin
import data

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

# connect to kucoin futures broker
exchange = ccxt.kucoinfutures({
    'apiKey': API_KEY,
    'apiSecret': API_SECRET,
    'password': API_PASSWORD
})


async def main():
    # load market data
    await exchange.load_markets()

    # get price data
    await data.get_candle_data(exchange, watchlist, '1h')

    # get ohlc candles
    for coin in watchlist.values():
        coin.candles = data.get_ohlc_candle_data(coin.raw_data)
    
    # calculate 5 EMA 10 EMA and 30 EMA

    # determine whether to LONG, SHORT, or HOLD
    
    # print(watchlist['ftm'].candles['close'])
    await exchange.close()

asyncio.run(main())