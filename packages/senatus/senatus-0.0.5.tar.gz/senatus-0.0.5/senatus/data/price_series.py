import pandas as pd
from .candlestick import Candlestick

class PriceSeries:
    
    candles: pd.DataFrame
    pair: str
    timeframe: str

    def __init__(
        self,
        candlesticks: list[Candlestick],
        pair: str,
        timeframe: str,
    ):  
        # Need to throw an error with invalid candlesticks (like null list)
        self.candles = Candlestick.to_dataframe(candlesticks)
        self.pair = pair
        self.timeframe = timeframe
        self.candles['timestamp'] = pd.to_datetime(self.candles['timestamp'])
        self.candles.set_index('timestamp', inplace=True)

    