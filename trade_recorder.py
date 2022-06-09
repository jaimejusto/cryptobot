import pandas as pd
import os.path


COL_NAMES = ['ID', 'DATE_OPEN', 'DATE_CLOSE', 'COIN', 'SIDE', 'ENTRY', 'EXIT', 'PNL(%)']
FILENAME = 'trade_history.xlsx'

def document_trade(trade_data):
    # No trade occured
    if trade_data == False: 
        return

    # Trade was closed, update columns
    if trade_data['date_close'] != None:
        previous_trade_data = pd.read_excel(FILENAME)
        
        # update date_close, exit and pnl cells
        print(previous_trade_data)

    # Trade was opened, append to file
    else:
        global last_row

        if os.path.exists(FILENAME):
            previous_trade_data = pd.read_excel(FILENAME)
            new_trade_data = pd.DataFrame([trade_data])
            updated_data = pd.concat([previous_trade_data, new_trade_data])
            updated_data.to_excel(FILENAME, index=False)
        else:
            df = pd.DataFrame([trade_data])
            df.to_excel(FILENAME, index=False)