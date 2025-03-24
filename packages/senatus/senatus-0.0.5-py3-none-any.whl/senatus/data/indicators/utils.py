import numpy as np
import pandas as pd

def calcSMA(data: pd.Series, period: int):
    return data.rolling(window=period).mean() 

def calcRSI(close: pd.Series, window: int = 14): 
        delta = close.diff()
        avg_gain = calcSMA(delta.where(delta >= 0, 0))
        avg_loss = calcSMA(-delta.where(delta < 0, 0))
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

def calcSMMA(data: pd.Series, period: int):
    #Evaluate the SMMA for each data point
    def evalSMMA(index, value, prev, period):
        if index < period - 1:
            return 0
        if index == period - 1:
            return data[:period].mean()
        return (prev * (period - 1) + value) / period
    smma = pd.Series(dtype=float)
    for i in range(len(data)):
         prev = smma[i - 1] if i > 0 else 0
         smma.loc[i] = (evalSMMA(i, data.iloc[i], prev, period))
    return smma

def calcWRSI(data: pd.Series, period: int):
    #Calculates the Wilder's RSI with his smoothing method (RSI used in Tranding View)
    delta = data.diff()
    ups = delta.where(delta >= 0, 0)
    downs = abs(delta.where(delta < 0, 0))     #Loss values should be treated as positive for calculation
    smmaU = calcSMMA(ups, period)
    smmaD = calcSMMA(downs, period)
    rs = smmaU.div(smmaD.replace(0, np.nan), fill_value=0)  # Avoid division by zero
    return rs.apply(lambda elem: 100 - (100/(1+elem)))