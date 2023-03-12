import pandas as pd
import os

def load_symbols_csv_to_db(connection, file_path: str = './data/symbols_valid_meta.csv'):
    '''
    Loading the symbols csv file and returning as a Pandas DataFrame.
    '''
    df = pd.read_csv(file_path)
    connection.write_table(df)
    

def load_stock_price_to_db(connection, file_path: str = './data/stocks/'):
    dir_list = os.listdir(file_path)
    for f in dir_list:
        full_path = os.path.join(file_path, f)
        try:
            df = pd.read_csv(full_path)
            df['ticker'] = f.split('.')[0]
            df['is_stock'] = 1
            df = df.rename({
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Adj Close': 'adj_close', 
                'Volume': 'volume'
            }, axis = 1)
            df = df[[
                'ticker', 'is_stock', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'
            ]]
            connection.write_table(df)
        except Exception as e:
            print(f)
            print(e)

def load_etf_price_to_db(connection, file_path: str = './data/etfs/'):
    dir_list = os.listdir(file_path)
    for f in dir_list:
        full_path = os.path.join(file_path, f)
        try:
            df = pd.read_csv(full_path)
            df['ticker'] = f.split('.')[0]
            df['is_stock'] = 0
            df = df.rename({
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Adj Close': 'adj_close', 
                'Volume': 'volume'
            }, axis = 1)
            df = df[[
                'ticker', 'is_stock', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'
            ]]
            connection.write_table(df)
        except Exception as e:
            print(f)
            print(e)