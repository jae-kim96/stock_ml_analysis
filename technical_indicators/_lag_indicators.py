import pandas as pd
import numpy as np

def calc_sma(df: pd.DataFrame, n_days: list = [50, 200]):
    '''
    A function to calculate the Simple Moving Average for each stock ticker in the dataset.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe with the prices data, must include adj_close and ticker columns
    n_days: list, optional
        The window for the Moving Average calculation

    Return
    ------
    df: pd.DataFrame
        The dataframe with the SMA in the columns
    '''
    ## Calculating the SMAs
    for n in n_days:
        df[f'sma_{n}'] = df.groupby('ticker')['adj_close'].transform(lambda x: x.rolling(n).mean())
    
    return df.reset_index(drop = True)


def calc_ema(df: pd.DataFrame, n_days: list = [12, 16, 50, 200]):
    '''
    A function to calculate the Exponential Moving Average for each stock ticker in the dataset.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe with the prices data, must include adj_close and ticker columns
    n_days: list, optional
        The window for the Moving Average calculation

    Return
    ------
    df: pd.DataFrame
        The dataframe with the EMA in the columns
    '''
    for n in n_days:
        df[f'ema_{n}'] = df.groupby('ticker')['adj_close'].transform(lambda x: x.ewm(span = n, min_periods = n, adjust = False).mean())

    return df.reset_index(drop = True)

def calc_bollinger_bands(df: pd.DataFrame, n_days: int = 20, stds: int = 2):
    '''
    A function to calculate the Bollinger Bands for each stock ticker in the dataset.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe with the prices data, must include adj_close and ticker columns
    n_days: int, optional
        The window for the Moving Average calculation
    stds: int, optional
        The number of standard deviations for the bands calculation

    Return
    ------
    df: pd.DataFrame
        The dataframe with the Bollinger Bands in the columns
    '''
    df[f'bb_upper_{n_days}'] = df.groupby('ticker')['adj_close'].transform(lambda x: x.rolling(n_days).mean() + stds * x.rolling(n_days).std())
    df[f'bb_lower_{n_days}'] = df.groupby('ticker')['adj_close'].transform(lambda x: x.rolling(n_days).mean() - stds * x.rolling(n_days).std())

    return df.reset_index(drop = True)

def calc_macd(df: pd.DataFrame, n_days: list = [12, 26], signal: int = 9):
    '''
    A function to calculate the MACD Indicator for each stock ticker in the dataset.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe with the prices data, must include adj_close and ticker columns
    n_days: list, optional
        The window for the Moving Average calculation

    Return
    ------
    df: pd.DataFrame
        The dataframe with the MACD in the columns
    '''
    col_names = [f'ema_{x}' for x in n_days]
    for n in n_days:
        if f'ema_{n}' not in df.columns:
            df[f'ema_{n}'] = df.groupby('ticker')['adj_close'].transform(lambda x: x.ewm(span = n, min_periods = n, adjust = False).mean())
    df[f'macd_{n_days[0]}-{n_days[1]}'] = df[f'ema_{n_days[0]}'] - df[f'ema_{n_days[1]}']
    df[f'macd_signal_{signal}'] = df.groupby('ticker')['adj_close'].transform(lambda x: x.ewm(span = signal, min_periods = signal, adjust = False).mean())

    return df

def calc_rsi(df: pd.DataFrame, n_days: list = [14]):
    '''
    A function to calculate the RSI for each stock ticker in the dataset.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe with the prices data, must include adj_close and ticker columns
    n_days: int, optional
        The window for the Moving Average calculation

    Return
    ------
    df: pd.DataFrame
        The dataframe with the RSI in the columns
    '''
    for n in n_days:
        df['delta'] = df.groupby('ticker')['adj_close'].diff()
        df['up'] = df.delta.clip(lower = 0)
        df['down'] = -1 * df.delta.clip(upper = 0)
        df['ema_up'] = df.groupby('ticker')['up'].transform(lambda x: x.ewm(span = n, min_periods = n, adjust = False).mean())
        df['ema_down'] = df.groupby('ticker')['down'].transform(lambda x: x.ewm(span = n, min_periods = n, adjust = False).mean())
        df['rs'] = df.ema_up / df.ema_down
        df[f'rsi_{n_days}'] = 100 - (100 / (1 + df.rs))

        df.drop(['delta', 'up', 'down', 'ema_up','ema_down', 'rs'], axis = 1, inplace = True)

    return df.reset_index(drop = True)