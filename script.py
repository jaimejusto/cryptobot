import os
import time
from  dotenv import load_dotenv
import asyncio
import ccxt.async_support as ccxt
from coin import Coin
import trading_helpers.ccxt_helper as ccxt_helper
import trading_strategies as strategies
import trade_recorder as record


# load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
API_PASSWORD = os.getenv('API_PW')

BULLISH = 1
BEARISH = -1
FILENAME = 'trade_history.xlsx'
LEVERAGE = 5
RISK_PER_TRADE = 0.4

# connect to kucoin futures broker
exchange = ccxt.kucoinfutures({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'password': API_PASSWORD
})

# coins to monitor
coin_symbols = [
    'ADA/USDT:USDT',
    'APE/USDT:USDT',
    'AVAX/USDT:USDT',
    'BTC/USDT:USDT',
    'ETH/USDT:USDT',
    'FTM/USDT:USDT',
    'SOL/USDT:USDT',
    'XRP/USDT:USDT'
]


async def main():
    # load market data
    await exchange.load_markets()

    # create watchlist of coins that retrieves data for perp market
    watchlist = ccxt_helper.get_coins_contract_data(exchange, coin_symbols)

    paper_balance = Coin.get_paper_balance()
    trade_number = Coin.get_trade_id()

    while trade_number != 100:
        print(f'TRADING with ${paper_balance}...')

        for coin in watchlist.values():    
            # get price data
            coin.candles, coin.marketprice = await ccxt_helper.get_price_data(exchange, coin.symbol, '1m')
            
            # trade using two ema strategy
            coin.market_sentiment = strategies.two_ema_strategy(coin)

            # execute trade
            trade_data = ccxt_helper.execute_papertrade(coin, paper_balance, RISK_PER_TRADE, LEVERAGE)
            paper_balance = Coin.get_paper_balance()

            # document the trade
            record.document_trade(FILENAME, trade_data)

            # display available balance
            print(f'Balance available: ${paper_balance}')
        # run every 5 minutes (300 seconds)
        print('--watching---')
        trade_number = Coin.get_trade_id()
        time.sleep(120)

    await exchange.close()

asyncio.run(main())