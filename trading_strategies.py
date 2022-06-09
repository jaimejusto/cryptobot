import tulipy as ti

BULLISH = 'long'
BEARISH = 'short'

def two_ema_strategy(coin):
    """ Conditions to (enter long) / (exit short) position:
            1. 12 EMA is above 26 EMA
        Conditions to (exit long) / (enter short):
            1. 12 EMA is below 26 EMA
    """
    # calculate 12 EMA and 26 EMA
    coin.ema_12 = ti.ema(coin.candles['close'], period=12)
    coin.ema_26 = ti.ema(coin.candles['close'], period=26)

    # select current ema data
    current_ema_12 = coin.ema_12[-1]
    current_ema_26 = coin.ema_26[-1]

    if current_ema_12 > current_ema_26:
        return BULLISH
    elif current_ema_12 < current_ema_26:
        return BEARISH

