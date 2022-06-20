import requests
import time

# variables for Kucoin Futures API
BASE_URL = 'https://api-futures.kucoin.com'


signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())