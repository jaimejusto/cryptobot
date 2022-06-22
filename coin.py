from datetime import datetime
class Coin:
    trade_id = 0
    def __init__(self, symbol, contract_size, min_leverage, max_leverage):
        self.symbol  = symbol
        self.raw_data = []
        self.market_sentiment = None
        self.marketprice = {
            'bid': None,
            'ask': None
        }
        self.position = {
            'trade_id': None,
            'isOpen': False,
            'side': None
        }
        self.leverage_limits = {
            'min': min_leverage,
            'max': max_leverage
        }
        self.contract_size = contract_size

    @staticmethod
    def get_trade_id():
        return Coin.trade_id

    def get_marketorder_price(self):
        return self.marketprice['ask'] if self.market_sentiment == 'long' else self.marketprice['bid']

    def assign_id(self):
        Coin.trade_id += 1
        self.position['trade_id'] = Coin.trade_id
    
    def open_trade(self):
        self.position['side'] = self.market_sentiment
        self.assign_id()
        self.position['isOpen'] = True
        return {
            'trade_id': self.position['trade_id'], 
            'date_open': datetime.now(), 
            'date_close': None,
            'symbol': self.symbol, 
            'side': self.position['side'], 
            'entry': self.get_marketorder_price(),
            'exit': None
        }

    def close_trade(self):
        self.position['side'] = None
        self.position['isOpen'] = False
        return {
            'trade_id': self.position['trade_id'],
            'date_close': datetime.now(),
            'exit': self.get_marketorder_price()
        }

    def open_position_contradicts_sentiment(self):
        if self.position['isOpen'] and (self.position['side'] != self.market_sentiment):
            return True

        return False