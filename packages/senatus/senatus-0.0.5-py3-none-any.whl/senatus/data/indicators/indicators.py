import pandas as pd
from .. import PriceSeries
from .utils import (
    calcRSI, 
    calcWRSI,
)

def getMAV(ps: PriceSeries, period: int = 20):
    df = ps.candles
    return pd.DataFrame({
        'Date': df.index,
        'Value': df['close'].rolling(window=period).mean()
    }).set_index('Date')

def getEMA(ps: PriceSeries, period: int = 20):
    df = ps.candles
    return pd.DataFrame({
        'Date': df.index,
        'Value': df['close'].ewm(span=period, adjust=False).mean()
    }).set_index('Date')

def getRSI(ps: PriceSeries, period: int = 14):
    df = ps.candles
    #Ensure 'close' column is numeric
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['Value'] = calcRSI(df['close'], period)
    return df[['Value']]

def getWRSI(ps: PriceSeries, period: int = 14):
    df = ps.candles
    #Ensure 'close' column is numeric
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['Value'] = calcWRSI(df['close'], period).values
    return df[['Value']]