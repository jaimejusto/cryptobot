class Coin:
    trade_id = 0
    def __init__(self, symbol):
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
            'side': None,
            'raw_data': {}
        }

    def get_marketorder_price(self):
        return self.marketprice['ask'] if self.market_sentiment == 'long' else self.marketprice['bid']

    def increase_id(self):
        Coin.trade_id += 1
        self.position['trade_id'] = Coin.trade_id