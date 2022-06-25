import pandas as pd
import os.path


INDEX_LABEL = 'trade_id'

def document_trade(file, trade_data):
    # No trade occured
    if not trade_occured(trade_data):
        return
    
    # Trade was opened, add to history
    if position_was_opened(trade_data):
        add_position(file, trade_data['opened_position'])
    
    # Trade was closed, update history
    if position_was_closed(trade_data):
        update_position(file, trade_data['closed_position'])

def trade_occured(trade_data):
    return bool(trade_data)

def position_was_opened(trade_data):
    if 'opened_position' in trade_data:
        return True
    
    return False

def position_was_closed(trade_data):
    if 'closed_position' in trade_data:
        return True
    
    return False

def add_position(file, trade_data):
    if os.path.exists(file):
        previous_trade_data = pd.read_excel(file)
        new_trade_data = pd.DataFrame([trade_data])
        updated_data = pd.concat([previous_trade_data, new_trade_data])
        updated_data.to_excel(file, index=False)

    else:
        first_trade = pd.DataFrame([trade_data])
        first_trade.to_excel(file, index=False)
        
def update_position(file, trade_data):
    trade_history = pd.read_excel(file)
    trade_history.set_index(INDEX_LABEL, inplace=True)
    position = trade_history.loc[trade_data['trade_id']]        # position to close
    final_data = get_finalized_data(position, trade_data)       # returns [date_close, exit, pnl]

    # update date_close, exit and pnl cells
    trade_history.loc[trade_data['trade_id'], ['date_close', 'exit', 'pnl']] = final_data
    trade_history.to_excel(file)

def get_finalized_data(position, trade_data):
    # get pnl
    pnl = calc_pnl_dollars(position['entry'], trade_data['exit'], position['side'], position['quantity'])
    return [trade_data['date_close'], trade_data['exit'], pnl]

def calc_pnl_dollars(entry, exit, side, quantity):
    pnl = (exit - entry) * quantity

    if side == 'short':
        pnl *= -1

    return pnl
