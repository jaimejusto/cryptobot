import os
import time
from  dotenv import load_dotenv
import asyncio
import ccxt.async_support as ccxt
from coin import Coin
import data
import trading_strategies as trade
import trade_recorder as record


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
FILENAME = 'trade_history.xlsx'

# connect to kucoin futures broker
exchange = ccxt.kucoinfutures({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'password': API_PASSWORD
})


async def main():
    # load market data
    await exchange.load_markets()

    # open file to documen trade history
    # record.create_file(FILENAME)

    while True:
        # get price data
        await data.get_candle_data(exchange, watchlist, '1m')
        print('TRADING...')

        for coin in watchlist.values():
            # get ohlc candles
            coin.candles = data.get_ohlc_candle_data(coin.raw_data)

            # get bid and ask price
            coin.marketprice = await data.get_bid_ask(exchange, coin.symbol)
            
            # trade using two ema strategy
            coin.market_sentiment = trade.two_ema_strategy(coin)

            # execute trade
            trade_data = data.execute_papertrade(coin)

            # document the trade
            record.document_trade(FILENAME, trade_data)

        # run every 5 minutes (300 seconds)
        print('--------')
        time.sleep(120)

    await exchange.close()

asyncio.run(main())