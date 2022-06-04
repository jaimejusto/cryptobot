import os
import ccxt.async_support as ccxt
from  dotenv import load_dotenv

# load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
API_PASSWORD = os.getenv('API_PW')

# connect to kucoin futures broker
exchange = ccxt.kucoinfutures({
    'apiKey': API_KEY,
    'apiSecret': API_SECRET,
    'password': API_PASSWORD
})


# get price data

# calculate 8 EMA and 31 EMA

# determine whether to LONG, SHORT, or HOLD