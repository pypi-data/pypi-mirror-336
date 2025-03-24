import pandas as pd

class Candlestick:
    """
    A candlestick representation
    """

    def __init__(
        self,
        timestamp: pd.Timestamp,    # Timestamps for date
        open: float,                # Open prices
        high: float,                # High prices
        low: float,                 # Low prices
        close: float,               # Close prices
        volume: float,              # Volume data
    ):
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __repr__(self):
        return f"{self.timestamp} {self.open} {self.high} {self.low} {self.close} {self.volume})"
    
    @classmethod
    def to_dataframe(cls, candlesticks):
        return pd.DataFrame({
            'timestamp': [candle.timestamp for candle in candlesticks],
            'open': [candle.open for candle in candlesticks],
            'high': [candle.high for candle in candlesticks],
            'low': [candle.low for candle in candlesticks],
            'close': [candle.close for candle in candlesticks],
            'volume': [candle.volume for candle in candlesticks] 
        })
