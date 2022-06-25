from datetime import datetime
class Coin:
    trade_id = 0
    paper_balance = 100

    def __init__(self, symbol, contract_size, min_leverage, max_leverage, taker_fee_rate):
        self.symbol  = symbol
        self.raw_data = []
        self.market_sentiment = None
        self.marketprice = {
            'bid': None,
            'ask': None
        }
        self.position = {
            'trade_id': None,
            'funds_used': None,
            'isOpen': False,
            'side': None,
            'position': None,
            'entry': None,
            'exit': None
        }
        self.leverage_limits = {
            'min': min_leverage,
            'max': max_leverage
        }
        self.contract_size = contract_size
        self.taker_fee_rate = taker_fee_rate

    @staticmethod
    def get_trade_id():
        return Coin.trade_id

    def get_marketorder_price(self):
        return self.marketprice['ask'] if self.position['side'] == 'long' else self.marketprice['bid']

    def assign_id(self):
        Coin.trade_id += 1
        self.position['trade_id'] = Coin.trade_id
    
    def has_open_position(self):
        return self.position['isOpen']
    
    def open_trade(self, funds_required, position_size):
        self._initialize_position(position_size, funds_required)
        Coin.paper_balance -= funds_required
        return {
            'trade_id': self.position['trade_id'], 
            'date_open': datetime.now(), 
            'date_close': None,
            'symbol': self.symbol, 
            'side': self.position['side'],
            'quantity': self.position['quantity'],
            'entry': self.position['entry'],
            'cost': position_size * self.position['entry'],
            'exit': None
        }

    def close_trade(self):
        self.position['exit'] = self.get_marketorder_price()
        pnl = self.calculate_pnl()
        self.position['side'] = None
        self.position['isOpen'] = False
        Coin.paper_balance += self.position['funds_used'] + pnl
        return {
            'trade_id': self.position['trade_id'],
            'date_close': datetime.now(),
            'exit': self.position['exit'],
            'pnl': pnl
        }

    def open_position_contradicts_sentiment(self):
        if self.position['isOpen'] and (self.position['side'] != self.market_sentiment):
            return True

        return False

    def get_contract_cost(self):
        return self.contract_size * self.get_marketorder_price()
    
    def _initialize_position(self, position_size, funds_used):
        self.position['side'] = self.market_sentiment
        self.assign_id()
        self.position['isOpen'] = True
        self.position['entry'] = self.get_marketorder_price()
        self.position['quantity'] = position_size
        self.position['funds_used'] = funds_used

    @staticmethod
    def get_paper_balance():
        return Coin.paper_balance
    
    def calculate_pnl(self):
        pnl = (self.position['exit'] - self.position['entry']) * self.position['quantity']

        if self.position['side'] == 'short':
            pnl *= -1

        return pnl
