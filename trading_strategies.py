def two_ema_strategy(ema_12, ema_26):
    """ Conditions to (enter long) / (exit short) position:
            1. 12 EMA is above 26 EMA on 5 minute chart
        Conditions to (exit long) / (enter short):
            1. 12 EMA is below 26 EMA on 5 minute chart 
    """
    if ema_12 > ema_26:
        return 1
    elif ema_12 < ema_26:
        return -1