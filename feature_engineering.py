import pandas as pd
import numpy as np
from DB import DB
from technical_indicators import *

SQL_DATABASE = DB('stock_data.db')
SP500 = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
MA_DAYS = [5, 10, 15, 30] # Moving Average Calculations
RSI_DAYS = [14, 28]
FILTER_YEAR = 2017
FEATURE_TABLE = 'sp500_technical_indicator_features'
FUTURE_DAYS = 7 # Predict Upward or Downward Trend this many days later

def get_sp_500_companies(url = SP500) -> list:
    '''
    Getting a list of the SP 500 Companies
    '''
    table = pd.read_html(url)
    df = table[0]
    return list(df.Symbol.unique())

def get_stock_data(tickers: list) -> pd.DataFrame:
    '''
    Getting the stock data from the database
    '''
    where_clause = '('
    for i, ticker in enumerate(tickers):
        if i < len(tickers) - 1:
            where_clause += f"'{ticker}'" + ', '
        else:
            where_clause += f"'{ticker}'" + ')'
    
    sql = f'''
        SELECT *
        FROM stock_etf_prices
        WHERE ticker IN {where_clause}
    '''

    df = SQL_DATABASE.get_data(sql)
    df['date'] = pd.to_datetime(df['date'])
    return df

def create_indicators(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Creating the Lagging Technical Indicators to use in Modelling and Feature Analysis
    '''
    df1 = calc_sma(df, n_days = MA_DAYS)
    df2 = calc_ema(df1, n_days = MA_DAYS)
    df3 = calc_bollinger_bands(df2)
    df4 = calc_macd(df3)
    df5 = calc_rsi(df4, n_days = RSI_DAYS)

    final_df = df5.drop(['is_stock', 'open', 'high', 'low', 'close'], axis = 1).reset_index(drop = True)
    # final_df = final_df.loc[final_df.date.dt.year >= FILTER_YEAR].reset_index(drop = True)
    return final_df

def create_prediction_var(df):
    '''
    Creating the Predicted Variable for the Features Dataset
    '''
    df['shifted'] = df.groupby('ticker')['adj_close'].transform(lambda x: x.shift(-1 * FUTURE_DAYS))
    df['price_diff'] = df.shifted - df.adj_close
    df['upward_trend'] = np.where(df.price_diff > 0, 1, 0)
    df = df.drop(['shifted', 'price_diff'], axis = 1)
    return df

if __name__ == '__main__':
    tickers = get_sp_500_companies()
    df1 = get_stock_data(tickers)
    df2 = create_indicators(df1)
    final_df = create_prediction_var(df2)

    ## Write to Database
    SQL_DATABASE.write_table(final_df, FEATURE_TABLE)
